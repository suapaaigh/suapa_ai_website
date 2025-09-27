from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CopilotProject(models.Model):
    PROJECT_TYPES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('data', 'Data Science'),
        ('ai', 'AI/ML Project'),
        ('api', 'API Development'),
        ('general', 'General Programming'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('archived', 'Archived'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    programming_language = models.CharField(max_length=50, blank=True)
    framework = models.CharField(max_length=100, blank=True)
    repository_url = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Copilot Project"
        verbose_name_plural = "Copilot Projects"
        ordering = ['-updated_at']

class CopilotSession(models.Model):
    SESSION_TYPES = [
        ('coding', 'Coding Session'),
        ('debugging', 'Debugging'),
        ('review', 'Code Review'),
        ('planning', 'Project Planning'),
        ('learning', 'Learning Session'),
    ]

    project = models.ForeignKey(CopilotProject, on_delete=models.CASCADE, related_name='sessions')
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    title = models.CharField(max_length=200, blank=True)
    goal = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.session_type.title()} - {self.project.name}"

    class Meta:
        verbose_name = "Copilot Session"
        verbose_name_plural = "Copilot Sessions"
        ordering = ['-started_at']

class CopilotInteraction(models.Model):
    INTERACTION_TYPES = [
        ('question', 'Question'),
        ('code_generation', 'Code Generation'),
        ('code_explanation', 'Code Explanation'),
        ('bug_fix', 'Bug Fix'),
        ('optimization', 'Code Optimization'),
        ('suggestion', 'Suggestion'),
    ]

    session = models.ForeignKey(CopilotSession, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    user_input = models.TextField()
    copilot_response = models.TextField()
    code_snippet = models.TextField(blank=True)
    file_path = models.CharField(max_length=500, blank=True)
    line_number = models.IntegerField(null=True, blank=True)
    was_helpful = models.BooleanField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.interaction_type.title()} in {self.session}"

    class Meta:
        verbose_name = "Copilot Interaction"
        verbose_name_plural = "Copilot Interactions"
        ordering = ['timestamp']

class CopilotCodeSuggestion(models.Model):
    SUGGESTION_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('modified', 'Modified'),
    ]

    session = models.ForeignKey(CopilotSession, on_delete=models.CASCADE)
    original_code = models.TextField(blank=True)
    suggested_code = models.TextField()
    explanation = models.TextField(blank=True)
    file_path = models.CharField(max_length=500, blank=True)
    start_line = models.IntegerField(null=True, blank=True)
    end_line = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=SUGGESTION_STATUS, default='pending')
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Code suggestion for {self.session.project.name}"

    class Meta:
        verbose_name = "Copilot Code Suggestion"
        verbose_name_plural = "Copilot Code Suggestions"

class CopilotLearningProgress(models.Model):
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    technology = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    progress_percentage = models.IntegerField(default=0)
    topics_completed = models.JSONField(default=list, blank=True)
    last_practice_date = models.DateField(null=True, blank=True)
    total_practice_time = models.DurationField(default=timezone.timedelta)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.technology} ({self.skill_level})"

    class Meta:
        verbose_name = "Copilot Learning Progress"
        verbose_name_plural = "Copilot Learning Progress"
        unique_together = ['user', 'technology']
