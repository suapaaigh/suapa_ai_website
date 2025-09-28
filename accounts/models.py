from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    LEARNING_STYLE_CHOICES = [
        ('visual', 'Visual Learner'),
        ('auditory', 'Auditory Learner'),
        ('kinesthetic', 'Kinesthetic Learner'),
        ('reading', 'Reading/Writing Learner'),
        ('mixed', 'Mixed Learning Style'),
    ]

    EDUCATION_LEVEL_CHOICES = [
        ('nursery', 'Nursery'),
        ('primary', 'Primary'),
        ('jhs', 'Junior High School'),
        ('shs', 'Senior High School'),
        ('tertiary', 'Tertiary'),
        ('adult', 'Adult Education'),
    ]

    REGION_CHOICES = [
        ('greater_accra', 'Greater Accra'),
        ('ashanti', 'Ashanti'),
        ('central', 'Central'),
        ('eastern', 'Eastern'),
        ('northern', 'Northern'),
        ('upper_east', 'Upper East'),
        ('upper_west', 'Upper West'),
        ('volta', 'Volta'),
        ('western', 'Western'),
        ('western_north', 'Western North'),
        ('bono', 'Bono'),
        ('bono_east', 'Bono East'),
        ('ahafo', 'Ahafo'),
        ('savannah', 'Savannah'),
        ('north_east', 'North East'),
        ('oti', 'Oti'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=20, choices=REGION_CHOICES, blank=True)
    website = models.URLField(blank=True)

    # Educational fields
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, blank=True)
    learning_style = models.CharField(max_length=20, choices=LEARNING_STYLE_CHOICES, blank=True)
    grade_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], null=True, blank=True)
    school_name = models.CharField(max_length=200, blank=True)
    preferred_language = models.CharField(max_length=50, default='english')

    # Learning preferences
    study_time_preference = models.CharField(max_length=20, choices=[
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('night', 'Night'),
        ('flexible', 'Flexible'),
    ], default='flexible')

    difficulty_preference = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('mixed', 'Mixed Levels'),
    ], default='beginner')

    # Goals and interests
    learning_goals = models.TextField(blank=True, help_text="What do you want to achieve?")
    interests = models.TextField(blank=True, help_text="Subjects or topics you're interested in")

    # Profile completion
    profile_completed = models.BooleanField(default=False)
    onboarding_completed = models.BooleanField(default=False)

    is_premium = models.BooleanField(default=False)
    premium_expiry = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    def get_suggested_subjects(self):
        from .utils import get_subjects_for_level
        return get_subjects_for_level(self.education_level, self.grade_level)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan} ({self.status})"

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

class UserEducationProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='education_profile')

    # Subject preferences and strengths
    favorite_subjects = models.ManyToManyField('companion.KnowledgeArea', blank=True, related_name='favorite_by_users')
    strong_subjects = models.ManyToManyField('companion.KnowledgeArea', blank=True, related_name='strong_in_users')
    weak_subjects = models.ManyToManyField('companion.KnowledgeArea', blank=True, related_name='weak_in_users')

    # Learning behavior patterns
    average_study_session = models.IntegerField(default=30, help_text="Average study session in minutes")
    preferred_content_types = models.JSONField(default=list, help_text="Preferred types of content (video, text, quiz, etc.)")
    learning_pace = models.CharField(max_length=20, choices=[
        ('slow', 'Slow and Steady'),
        ('moderate', 'Moderate'),
        ('fast', 'Fast Learner'),
        ('adaptive', 'Adaptive'),
    ], default='moderate')

    # Motivational factors
    motivation_type = models.CharField(max_length=20, choices=[
        ('achievement', 'Achievement Oriented'),
        ('competition', 'Competition Driven'),
        ('collaboration', 'Collaboration Focused'),
        ('exploration', 'Exploration Driven'),
        ('goal_oriented', 'Goal Oriented'),
    ], default='achievement')

    # Accessibility and special needs
    accessibility_needs = models.JSONField(default=list, help_text="Any accessibility requirements")
    special_considerations = models.TextField(blank=True, help_text="Special learning considerations")

    # Performance tracking
    overall_performance = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    improvement_rate = models.FloatField(default=0.0, help_text="Rate of improvement over time")
    consistency_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    # Adaptive learning parameters
    difficulty_adaptation = models.FloatField(default=0.0, help_text="Current difficulty adjustment")
    content_recommendation_weights = models.JSONField(default=dict, help_text="Weights for content recommendation algorithm")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Education Profile - {self.user_profile.user.username}"

    def get_recommended_subjects(self):
        from companion.models import KnowledgeArea
        user_level = self.user_profile.education_level
        user_grade = self.user_profile.grade_level

        subjects = KnowledgeArea.objects.filter(
            education_level=user_level,
            is_active=True
        )

        if user_grade:
            subjects = subjects.filter(grade_levels__contains=[user_grade])

        return subjects.exclude(id__in=self.weak_subjects.values_list('id', flat=True))

    def update_performance_metrics(self):
        from companion.models import UserLearningProgress
        progress_records = UserLearningProgress.objects.filter(user=self.user_profile.user)

        if progress_records.exists():
            avg_progress = progress_records.aggregate(
                avg_score=models.Avg('average_score'),
                avg_progress=models.Avg('progress_percentage')
            )

            self.overall_performance = (avg_progress['avg_score'] or 0 + avg_progress['avg_progress'] or 0) / 2
            self.save()

    class Meta:
        verbose_name = "User Education Profile"
        verbose_name_plural = "User Education Profiles"
