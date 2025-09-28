from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class CompanionPersonality(models.Model):
    PERSONALITY_TYPES = [
        ('friendly', 'Friendly'),
        ('professional', 'Professional'),
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('humorous', 'Humorous'),
        ('supportive', 'Supportive'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    personality_type = models.CharField(max_length=20, choices=PERSONALITY_TYPES)
    avatar = models.ImageField(upload_to='companion_avatars/', null=True, blank=True)
    traits = models.JSONField(default=list, blank=True)
    system_prompt = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Companion Personality"
        verbose_name_plural = "Companion Personalities"

class Companion(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
        ('maintenance', 'Maintenance'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    personality = models.ForeignKey(CompanionPersonality, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    custom_instructions = models.TextField(blank=True)
    learning_enabled = models.BooleanField(default=True)
    memory_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}'s companion"

    class Meta:
        verbose_name = "Companion"
        verbose_name_plural = "Companions"

class CompanionConversation(models.Model):
    companion = models.ForeignKey(Companion, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    topic = models.CharField(max_length=100, blank=True)
    mood = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation with {self.companion.name}"

    class Meta:
        verbose_name = "Companion Conversation"
        verbose_name_plural = "Companion Conversations"
        ordering = ['-updated_at']

class CompanionMessage(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('companion', 'Companion'),
        ('system', 'System'),
    ]

    conversation = models.ForeignKey(CompanionConversation, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    content = models.TextField()
    emotion = models.CharField(max_length=50, blank=True)
    context = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.message_type.title()} message in {self.conversation}"

    class Meta:
        verbose_name = "Companion Message"
        verbose_name_plural = "Companion Messages"
        ordering = ['timestamp']

class CompanionMemory(models.Model):
    MEMORY_TYPES = [
        ('personal', 'Personal Information'),
        ('preference', 'User Preference'),
        ('conversation', 'Conversation Context'),
        ('event', 'Important Event'),
        ('goal', 'User Goal'),
    ]

    companion = models.ForeignKey(Companion, on_delete=models.CASCADE, related_name='memories')
    memory_type = models.CharField(max_length=20, choices=MEMORY_TYPES)
    content = models.TextField()
    importance = models.IntegerField(default=1)
    last_accessed = models.DateTimeField(default=timezone.now)
    access_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.companion.name} - {self.memory_type} memory"

    class Meta:
        verbose_name = "Companion Memory"
        verbose_name_plural = "Companion Memories"
        ordering = ['-importance', '-last_accessed']

class KnowledgeArea(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('nursery', 'Nursery'),
        ('primary', 'Primary'),
        ('jhs', 'Junior High School'),
        ('shs', 'Senior High School'),
        ('tertiary', 'Tertiary'),
    ]

    SUBJECT_CATEGORY_CHOICES = [
        ('core', 'Core Subject'),
        ('elective', 'Elective Subject'),
        ('vocational', 'Vocational Subject'),
        ('extracurricular', 'Extracurricular'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    grade_levels = models.JSONField(default=list, help_text="List of applicable grade levels")
    subject_category = models.CharField(max_length=20, choices=SUBJECT_CATEGORY_CHOICES)

    # Ghanaian curriculum specific
    curriculum_code = models.CharField(max_length=20, blank=True, help_text="Official curriculum code")
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='leads_to')

    # Learning objectives and standards
    learning_objectives = models.JSONField(default=list, help_text="List of learning objectives")
    assessment_criteria = models.JSONField(default=list, help_text="Assessment criteria and standards")

    # Content organization
    topics = models.JSONField(default=list, help_text="Main topics covered in this subject")
    skills_developed = models.JSONField(default=list, help_text="Skills students develop")

    # Metadata
    is_active = models.BooleanField(default=True)
    difficulty_level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    estimated_hours = models.IntegerField(null=True, blank=True, help_text="Estimated learning hours")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.education_level})"

    def get_applicable_grades(self):
        return self.grade_levels

    def get_prerequisites_list(self):
        return list(self.prerequisites.values_list('name', flat=True))

    class Meta:
        verbose_name = "Knowledge Area"
        verbose_name_plural = "Knowledge Areas"
        ordering = ['education_level', 'name']
        unique_together = ['name', 'education_level']

class SubjectContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('lesson', 'Lesson'),
        ('exercise', 'Exercise'),
        ('quiz', 'Quiz'),
        ('project', 'Project'),
        ('resource', 'Resource'),
        ('video', 'Video'),
        ('reading', 'Reading Material'),
    ]

    DIFFICULTY_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    knowledge_area = models.ForeignKey(KnowledgeArea, on_delete=models.CASCADE, related_name='content')
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVEL_CHOICES)

    # Content details
    content_data = models.JSONField(default=dict, help_text="Structured content data")
    duration_minutes = models.IntegerField(null=True, blank=True)
    order_index = models.IntegerField(default=0)

    # Learning outcomes
    learning_outcomes = models.JSONField(default=list)
    tags = models.JSONField(default=list)

    # Adaptive learning
    success_rate = models.FloatField(default=0.0, help_text="Average success rate among users")
    engagement_score = models.FloatField(default=0.0, help_text="Average engagement score")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.knowledge_area.name}"

    class Meta:
        verbose_name = "Subject Content"
        verbose_name_plural = "Subject Contents"
        ordering = ['knowledge_area', 'order_index', 'title']

class UserLearningProgress(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('mastered', 'Mastered'),
        ('needs_review', 'Needs Review'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_progress')
    knowledge_area = models.ForeignKey(KnowledgeArea, on_delete=models.CASCADE)
    content = models.ForeignKey(SubjectContent, on_delete=models.CASCADE, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress_percentage = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Performance metrics
    attempts = models.IntegerField(default=0)
    best_score = models.FloatField(null=True, blank=True)
    average_score = models.FloatField(null=True, blank=True)
    time_spent_minutes = models.IntegerField(default=0)

    # Adaptive learning data
    difficulty_adjustment = models.FloatField(default=0.0, help_text="Adjustment factor for content difficulty")
    last_accessed = models.DateTimeField(null=True, blank=True)
    mastery_level = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.knowledge_area.name} ({self.status})"

    class Meta:
        verbose_name = "User Learning Progress"
        verbose_name_plural = "User Learning Progress"
        unique_together = ['user', 'knowledge_area', 'content']
        ordering = ['-updated_at']
