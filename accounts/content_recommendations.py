from django.db.models import Q, Avg, F
from companion.models import KnowledgeArea, SubjectContent, UserLearningProgress
from .models import UserProfile, UserEducationProfile
import random

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
        Get recommended subjects based on user's education level and preferences.
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
            subjects = subjects.filter(
                grade_levels__contains=[self.user_profile.grade_level]
            )

        # Exclude subjects the user is weak in (if they have education profile)
        if self.education_profile:
            weak_subject_ids = self.education_profile.weak_subjects.values_list('id', flat=True)
            subjects = subjects.exclude(id__in=weak_subject_ids)

        # Prioritize subjects based on user preferences
        recommended_subjects = list(subjects)

        # If user has favorite subjects, prioritize them
        if self.education_profile and self.education_profile.favorite_subjects.exists():
            favorite_subjects = list(self.education_profile.favorite_subjects.all())
            # Remove favorites from the main list and add them at the beginning
            for fav in favorite_subjects:
                if fav in recommended_subjects:
                    recommended_subjects.remove(fav)
            recommended_subjects = favorite_subjects + recommended_subjects

        return recommended_subjects[:limit]

    def get_recommended_content(self, subject=None, limit=20):
        """
        Get recommended content based on user's learning style and progress.
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

        # Filter by difficulty preference
        if self.user_profile.difficulty_preference != 'mixed':
            content_query = content_query.filter(
                difficulty_level=self.user_profile.difficulty_preference
            )

        # Filter by preferred content types if available
        if self.education_profile and self.education_profile.preferred_content_types:
            content_query = content_query.filter(
                content_type__in=self.education_profile.preferred_content_types
            )

        # Get user's progress to avoid already mastered content
        completed_content_ids = UserLearningProgress.objects.filter(
            user=self.user,
            status__in=['completed', 'mastered']
        ).values_list('content_id', flat=True)

        content_query = content_query.exclude(id__in=completed_content_ids)

        # Order by relevance and engagement
        content_query = content_query.order_by(
            '-engagement_score',
            '-success_rate',
            'order_index'
        )

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

    def get_daily_recommendations(self, limit=5):
        """
        Get daily content recommendations based on user's study preferences.
        """
        recommended_subjects = self.get_recommended_subjects(limit=3)
        daily_content = []

        for subject in recommended_subjects:
            # Get 1-2 pieces of content per subject
            content = self.get_adaptive_content(subject)[:2]
            for item in content:
                daily_content.append({
                    'content': item,
                    'subject': subject,
                    'reason': self._get_recommendation_reason(item, subject)
                })

        # Shuffle and limit
        random.shuffle(daily_content)
        return daily_content[:limit]

    def _get_recommendation_reason(self, content, subject):
        """
        Generate a reason for why this content is recommended.
        """
        reasons = []

        if self.education_profile:
            if subject in self.education_profile.favorite_subjects.all():
                reasons.append("This is one of your favorite subjects")

            if content.content_type in self.education_profile.preferred_content_types:
                reasons.append(f"Matches your preferred {content.content_type} learning style")

        if content.success_rate > 0.8:
            reasons.append("High success rate among learners")

        if content.engagement_score > 0.7:
            reasons.append("Highly engaging content")

        if not reasons:
            reasons.append("Recommended for your education level")

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