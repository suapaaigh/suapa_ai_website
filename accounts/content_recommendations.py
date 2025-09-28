from django.db.models import Q, Avg, F, Count, Case, When, IntegerField
from companion.models import KnowledgeArea, SubjectContent, UserLearningProgress
from .models import UserProfile, UserEducationProfile
import random
from datetime import datetime, timedelta
from django.utils import timezone

class ContentRecommendationEngine:
    """
    Advanced content recommendation system for educational content
    based on user profile, learning style, and progress.
    """

    def __init__(self, user):
        self.user = user
        try:
            self.user_profile = user.userprofile
            self.education_profile = user.userprofile.education_profile
        except (UserProfile.DoesNotExist, UserEducationProfile.DoesNotExist):
            self.user_profile = None
            self.education_profile = None

    def get_recommended_subjects(self, limit=10):
        """
        Get recommended subjects based on user's education level, preferences, and learning patterns.
        """
        if not self.user_profile:
            return KnowledgeArea.objects.filter(is_active=True)[:limit]

        # Base query for user's education level
        subjects = KnowledgeArea.objects.filter(
            education_level=self.user_profile.education_level,
            is_active=True
        )

        # Filter by grade level if specified
        if self.user_profile.grade_level:
            # Use icontains for SQLite compatibility
            subjects = subjects.filter(
                grade_levels__icontains=str(self.user_profile.grade_level)
            )

        if self.education_profile:
            # Exclude subjects the user is weak in
            weak_subject_ids = self.education_profile.weak_subjects.values_list('id', flat=True)
            subjects = subjects.exclude(id__in=weak_subject_ids)

            # Annotate subjects with user engagement and progress
            subjects = subjects.annotate(
                user_progress_count=Count(
                    'userlearningprogress',
                    filter=Q(userlearningprogress__user=self.user)
                ),
                user_avg_score=Avg(
                    'userlearningprogress__average_score',
                    filter=Q(userlearningprogress__user=self.user)
                ),
                is_favorite=Case(
                    When(id__in=self.education_profile.favorite_subjects.values_list('id', flat=True), then=1),
                    default=0,
                    output_field=IntegerField()
                ),
                is_strong=Case(
                    When(id__in=self.education_profile.strong_subjects.values_list('id', flat=True), then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )

            # Order by user preferences and engagement
            subjects = subjects.order_by(
                '-is_favorite',  # Favorite subjects first
                '-is_strong',    # Strong subjects next
                '-user_avg_score',  # Subjects with better performance
                '-user_progress_count',  # Subjects with more engagement
                'difficulty_level',  # Easier subjects first
                'name'
            )
        else:
            # For users without education profile, order by general metrics
            subjects = subjects.order_by('difficulty_level', 'name')

        return subjects[:limit]

    def get_recommended_content(self, subject=None, limit=20):
        """
        Get recommended content based on user's learning style, progress, and companion app data.
        """
        if not self.user_profile:
            # Return random content if no profile
            query = SubjectContent.objects.filter(is_active=True)
            if subject:
                query = query.filter(knowledge_area=subject)
            return query.order_by('?')[:limit]

        # Base query
        content_query = SubjectContent.objects.filter(is_active=True)

        if subject:
            content_query = content_query.filter(knowledge_area=subject)

        # Advanced filtering based on user profile
        if self.education_profile:
            # Filter by preferred content types
            if self.education_profile.preferred_content_types:
                content_query = content_query.filter(
                    content_type__in=self.education_profile.preferred_content_types
                )

            # Adaptive difficulty filtering based on performance
            user_avg_performance = self.education_profile.overall_performance
            if user_avg_performance >= 80:
                # High performer - show advanced content
                difficulty_order = ['advanced', 'intermediate', 'beginner']
            elif user_avg_performance >= 60:
                # Average performer - balanced mix
                difficulty_order = ['intermediate', 'beginner', 'advanced']
            else:
                # Struggling learner - focus on beginner content
                difficulty_order = ['beginner', 'intermediate']

            if self.user_profile.difficulty_preference != 'mixed':
                content_query = content_query.filter(
                    difficulty_level=self.user_profile.difficulty_preference
                )
            else:
                # Use performance-based difficulty ordering
                when_clauses = [When(difficulty_level=level, then=pos) for pos, level in enumerate(difficulty_order)]
                content_query = content_query.annotate(
                    difficulty_priority=Case(*when_clauses, default=99, output_field=IntegerField())
                )

        # Exclude already mastered content
        completed_content_ids = UserLearningProgress.objects.filter(
            user=self.user,
            status__in=['completed', 'mastered']
        ).values_list('content_id', flat=True)
        content_query = content_query.exclude(id__in=completed_content_ids)

        # Prioritize content based on user's recent learning patterns
        recent_progress = UserLearningProgress.objects.filter(
            user=self.user,
            updated_at__gte=timezone.now() - timedelta(days=7)
        ).values_list('knowledge_area_id', flat=True)

        if recent_progress:
            content_query = content_query.annotate(
                is_recent_subject=Case(
                    When(knowledge_area_id__in=recent_progress, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )

        # Order by multiple factors for personalized recommendations
        if self.education_profile:
            order_fields = [
                '-is_recent_subject',  # Continue recent subjects
                'difficulty_priority',  # Appropriate difficulty
                '-engagement_score',    # High engagement content
                '-success_rate',       # High success rate
                'order_index'          # Curriculum order
            ]
        else:
            order_fields = ['-engagement_score', '-success_rate', 'order_index']

        content_query = content_query.order_by(*order_fields)
        return content_query[:limit]

    def get_adaptive_content(self, subject, user_performance=None):
        """
        Get content adapted to user's current performance level.
        """
        if not self.education_profile:
            return self.get_recommended_content(subject)

        # Get user's current performance in this subject
        if user_performance is None:
            progress_records = UserLearningProgress.objects.filter(
                user=self.user,
                knowledge_area=subject
            )
            if progress_records.exists():
                user_performance = progress_records.aggregate(
                    avg_score=Avg('average_score')
                )['avg_score'] or 0
            else:
                user_performance = 0

        # Determine appropriate difficulty level
        if user_performance >= 80:
            target_difficulty = 'advanced'
        elif user_performance >= 60:
            target_difficulty = 'intermediate'
        else:
            target_difficulty = 'beginner'

        # Get content at appropriate difficulty
        content = SubjectContent.objects.filter(
            knowledge_area=subject,
            difficulty_level=target_difficulty,
            is_active=True
        )

        # If no content at target difficulty, get mixed difficulty
        if not content.exists():
            content = SubjectContent.objects.filter(
                knowledge_area=subject,
                is_active=True
            )

        return content.order_by('order_index', '-engagement_score')

    def get_learning_path(self, subject):
        """
        Generate a structured learning path for a subject.
        """
        # Get all content for the subject
        all_content = SubjectContent.objects.filter(
            knowledge_area=subject,
            is_active=True
        ).order_by('order_index', 'difficulty_level')

        # Get user's progress
        user_progress = UserLearningProgress.objects.filter(
            user=self.user,
            knowledge_area=subject
        ).values_list('content_id', 'status')

        progress_dict = dict(user_progress)

        # Organize content into a learning path
        learning_path = {
            'subject': subject,
            'total_content': all_content.count(),
            'completed_count': len([p for p in progress_dict.values() if p in ['completed', 'mastered']]),
            'content_groups': []
        }

        # Group content by difficulty level
        difficulty_levels = ['beginner', 'intermediate', 'advanced']
        for difficulty in difficulty_levels:
            difficulty_content = all_content.filter(difficulty_level=difficulty)
            if difficulty_content.exists():
                content_items = []
                for content in difficulty_content:
                    status = progress_dict.get(content.id, 'not_started')
                    content_items.append({
                        'content': content,
                        'status': status,
                        'is_accessible': self._is_content_accessible(content, progress_dict)
                    })

                learning_path['content_groups'].append({
                    'difficulty': difficulty,
                    'content_items': content_items
                })

        return learning_path

    def _is_content_accessible(self, content, progress_dict):
        """
        Determine if content is accessible based on prerequisites.
        """
        # Simple logic: content is accessible if it's beginner level
        # or if user has completed some content in the subject
        if content.difficulty_level == 'beginner':
            return True

        # Check if user has completed any beginner content
        completed_statuses = ['completed', 'mastered']
        has_completed_content = any(
            status in completed_statuses for status in progress_dict.values()
        )

        return has_completed_content

    def get_daily_recommendations(self, limit=8):
        """
        Get personalized daily content recommendations based on user's study preferences and patterns.
        """
        recommended_subjects = self.get_recommended_subjects(limit=5)
        daily_content = []

        # Determine content distribution based on user preferences
        if self.education_profile:
            content_per_subject = max(1, limit // len(recommended_subjects)) if recommended_subjects else 1

            # Factor in user's study session preference
            session_length = self.education_profile.average_study_session
            if session_length <= 20:
                # Short sessions - prefer quizzes and exercises
                preferred_types = ['quiz', 'exercise', 'lesson']
            elif session_length <= 45:
                # Medium sessions - balanced mix
                preferred_types = ['lesson', 'exercise', 'video', 'quiz']
            else:
                # Long sessions - comprehensive content
                preferred_types = ['video', 'lesson', 'project', 'reading']
        else:
            content_per_subject = 2
            preferred_types = ['lesson', 'quiz', 'video']

        for subject in recommended_subjects:
            # Get adaptive content for each subject
            content = self.get_adaptive_content(subject, limit=content_per_subject * 2)

            # Filter by preferred content types if available
            if self.education_profile and preferred_types:
                type_filtered = [c for c in content if c.content_type in preferred_types]
                if type_filtered:
                    content = type_filtered

            # Select content for this subject
            selected_content = content[:content_per_subject]

            for item in selected_content:
                daily_content.append({
                    'content': item,
                    'subject': subject,
                    'reason': self._get_recommendation_reason(item, subject),
                    'estimated_time': item.duration_minutes or 15,
                    'difficulty': item.difficulty_level,
                    'type': item.content_type
                })

        # Sort by priority and user preferences
        if self.education_profile:
            # Sort by motivation type
            if self.education_profile.motivation_type == 'achievement':
                daily_content.sort(key=lambda x: (x['difficulty'] == 'advanced', -x['estimated_time']))
            elif self.education_profile.motivation_type == 'exploration':
                random.shuffle(daily_content)
            else:
                daily_content.sort(key=lambda x: x['estimated_time'])
        else:
            random.shuffle(daily_content)

        return daily_content[:limit]

    def _get_recommendation_reason(self, content, subject):
        """
        Generate a personalized reason for why this content is recommended.
        """
        reasons = []

        if self.education_profile:
            # Check user preferences and patterns
            if subject in self.education_profile.favorite_subjects.all():
                reasons.append("This is one of your favorite subjects")

            if subject in self.education_profile.strong_subjects.all():
                reasons.append("Building on your strengths")

            if content.content_type in self.education_profile.preferred_content_types:
                content_type_display = content.get_content_type_display()
                reasons.append(f"Matches your preferred {content_type_display.lower()} learning style")

            # Check user's learning patterns
            if self.education_profile.learning_pace == 'fast' and content.difficulty_level == 'advanced':
                reasons.append("Challenging content for fast learners")
            elif self.education_profile.learning_pace == 'slow' and content.difficulty_level == 'beginner':
                reasons.append("Perfect pace for steady learning")

            # Check motivation type
            if self.education_profile.motivation_type == 'achievement' and content.success_rate > 0.8:
                reasons.append("High achievement potential")
            elif self.education_profile.motivation_type == 'exploration':
                reasons.append("Great for exploring new concepts")

        # Check recent user progress
        recent_progress = UserLearningProgress.objects.filter(
            user=self.user,
            knowledge_area=subject,
            updated_at__gte=timezone.now() - timedelta(days=3)
        ).exists()

        if recent_progress:
            reasons.append("Continue your recent progress")

        # Content quality indicators
        if content.success_rate > 0.8:
            reasons.append("High success rate among learners")

        if content.engagement_score > 0.7:
            reasons.append("Highly engaging content")

        # Time-based recommendations
        if self.user_profile and self.user_profile.study_time_preference != 'flexible':
            current_hour = timezone.now().hour
            if ((self.user_profile.study_time_preference == 'morning' and 6 <= current_hour < 12) or
                (self.user_profile.study_time_preference == 'afternoon' and 12 <= current_hour < 17) or
                (self.user_profile.study_time_preference == 'evening' and 17 <= current_hour < 21) or
                (self.user_profile.study_time_preference == 'night' and (current_hour >= 21 or current_hour < 6))):
                reasons.append("Perfect for your preferred study time")

        # Default reasons
        if not reasons:
            if self.user_profile:
                reasons.append(f"Recommended for {self.user_profile.get_education_level_display()} level")
            else:
                reasons.append("Recommended for your learning journey")

        return random.choice(reasons)

    def update_recommendations_based_on_interaction(self, content, interaction_type, score=None):
        """
        Update recommendation weights based on user interactions.
        """
        if not self.education_profile:
            return

        # Get current weights
        weights = self.education_profile.content_recommendation_weights or {}

        # Update weights based on interaction
        content_type = content.content_type
        subject_id = str(content.knowledge_area.id)

        if interaction_type == 'completed':
            weights[f'content_type_{content_type}'] = weights.get(f'content_type_{content_type}', 1.0) + 0.1
            weights[f'subject_{subject_id}'] = weights.get(f'subject_{subject_id}', 1.0) + 0.1

        elif interaction_type == 'skipped':
            weights[f'content_type_{content_type}'] = max(0.1, weights.get(f'content_type_{content_type}', 1.0) - 0.05)

        elif interaction_type == 'high_score' and score:
            if score >= 80:
                weights[f'difficulty_{content.difficulty_level}'] = weights.get(f'difficulty_{content.difficulty_level}', 1.0) + 0.1

        # Save updated weights
        self.education_profile.content_recommendation_weights = weights
        self.education_profile.save()

    def get_personalized_learning_path(self, subject):
        """
        Generate a personalized learning path based on user's profile and companion app data.
        """
        # Get base learning path
        base_path = self.get_learning_path(subject)

        if not self.education_profile:
            return base_path

        # Customize based on user's learning pace and preferences
        pace = self.education_profile.learning_pace
        motivation = self.education_profile.motivation_type

        # Adjust content ordering based on pace
        for group in base_path['content_groups']:
            if pace == 'fast':
                # Fast learners: start with more challenging content
                group['content_items'].sort(key=lambda x: (
                    x['content'].difficulty_level != 'advanced',
                    x['content'].order_index
                ))
            elif pace == 'slow':
                # Slow learners: more gradual progression
                group['content_items'].sort(key=lambda x: (
                    x['content'].difficulty_level == 'advanced',
                    x['content'].order_index
                ))

        # Add motivation-based recommendations
        if motivation == 'achievement':
            base_path['learning_tips'] = [
                "Set clear goals for each study session",
                "Track your progress regularly",
                "Challenge yourself with advanced content when ready"
            ]
        elif motivation == 'exploration':
            base_path['learning_tips'] = [
                "Try different types of content",
                "Explore related topics",
                "Follow your curiosity"
            ]
        elif motivation == 'collaboration':
            base_path['learning_tips'] = [
                "Consider group study sessions",
                "Share your progress with others",
                "Engage in discussions about the content"
            ]
        else:
            base_path['learning_tips'] = [
                "Take breaks when needed",
                "Review previous content regularly",
                "Celebrate small achievements"
            ]

        return base_path

    def get_content_recommendations_by_time(self, time_available_minutes=30):
        """
        Get content recommendations based on available study time.
        """
        if not self.user_profile:
            return []

        # Get subjects user is currently working on
        active_subjects = UserLearningProgress.objects.filter(
            user=self.user,
            status='in_progress'
        ).values_list('knowledge_area', flat=True).distinct()

        if not active_subjects:
            # If no active subjects, get recommended subjects
            active_subjects = [s.id for s in self.get_recommended_subjects(limit=3)]

        recommendations = []
        time_used = 0

        for subject_id in active_subjects:
            if time_used >= time_available_minutes:
                break

            try:
                subject = KnowledgeArea.objects.get(id=subject_id)
                content = self.get_adaptive_content(subject, limit=10)

                for item in content:
                    estimated_time = item.duration_minutes or 15
                    if time_used + estimated_time <= time_available_minutes:
                        recommendations.append({
                            'content': item,
                            'subject': subject,
                            'estimated_time': estimated_time,
                            'reason': self._get_recommendation_reason(item, subject)
                        })
                        time_used += estimated_time

                        if time_used >= time_available_minutes * 0.9:  # Use 90% of available time
                            break
            except KnowledgeArea.DoesNotExist:
                continue

        return recommendations

    def get_weakness_improvement_plan(self):
        """
        Generate a plan to improve on weak subjects based on companion app data.
        """
        if not self.education_profile:
            return []

        weak_subjects = self.education_profile.weak_subjects.all()
        if not weak_subjects:
            return []

        improvement_plan = []

        for subject in weak_subjects:
            # Get beginner-level content for weak subjects
            beginner_content = SubjectContent.objects.filter(
                knowledge_area=subject,
                difficulty_level='beginner',
                is_active=True
            ).order_by('order_index')[:3]

            # Check user's current progress in this subject
            user_progress = UserLearningProgress.objects.filter(
                user=self.user,
                knowledge_area=subject
            ).aggregate(
                avg_score=Avg('average_score'),
                total_attempts=Count('id')
            )

            improvement_plan.append({
                'subject': subject,
                'current_score': user_progress['avg_score'] or 0,
                'attempts': user_progress['total_attempts'] or 0,
                'recommended_content': beginner_content,
                'focus_areas': subject.learning_objectives[:3] if subject.learning_objectives else [],
                'estimated_improvement_time': len(beginner_content) * 20  # 20 minutes per content
            })

        return improvement_plan

    def get_streak_motivation_content(self):
        """
        Get content to maintain or build learning streaks.
        """
        if not self.user_profile:
            return []

        # Check user's recent learning activity
        recent_days = 7
        recent_activity = UserLearningProgress.objects.filter(
            user=self.user,
            updated_at__gte=timezone.now() - timedelta(days=recent_days)
        ).values('updated_at__date').distinct().count()

        if recent_activity >= 3:  # User has been active
            # Provide content to maintain streak
            return self.get_daily_recommendations(limit=3)
        else:
            # User needs motivation to restart
            easy_content = []
            subjects = self.get_recommended_subjects(limit=2)

            for subject in subjects:
                content = SubjectContent.objects.filter(
                    knowledge_area=subject,
                    difficulty_level='beginner',
                    duration_minutes__lte=15,
                    is_active=True
                ).order_by('-engagement_score')[:2]

                for item in content:
                    easy_content.append({
                        'content': item,
                        'subject': subject,
                        'reason': "Quick win to restart your learning streak!"
                    })

            return easy_content[:3]

def get_content_suggestions_for_user(user, limit=10):
    """
    Convenience function to get content suggestions for a user.
    """
    engine = ContentRecommendationEngine(user)
    return engine.get_daily_recommendations(limit=limit)

def get_subject_learning_path(user, subject):
    """
    Convenience function to get learning path for a subject.
    """
    engine = ContentRecommendationEngine(user)
    return engine.get_learning_path(subject)