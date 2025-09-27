from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AIModel(models.Model):
    MODEL_TYPES = [
        ('text', 'Text Generation'),
        ('image', 'Image Generation'),
        ('audio', 'Audio Processing'),
        ('video', 'Video Processing'),
        ('code', 'Code Generation'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    provider = models.CharField(max_length=50)
    model_id = models.CharField(max_length=100)
    api_endpoint = models.URLField(blank=True)
    max_tokens = models.IntegerField(default=2000)
    cost_per_token = models.DecimalField(max_digits=10, decimal_places=8, default=0.0)
    is_active = models.BooleanField(default=True)
    requires_api_key = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.provider})"

    class Meta:
        verbose_name = "AI Model"
        verbose_name_plural = "AI Models"

class AIRequest(models.Model):
    REQUEST_TYPES = [
        ('completion', 'Text Completion'),
        ('generation', 'Content Generation'),
        ('analysis', 'Content Analysis'),
        ('translation', 'Translation'),
        ('summarization', 'Summarization'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    prompt = models.TextField()
    response = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tokens_used = models.IntegerField(default=0)
    processing_time = models.FloatField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.request_type.title()} request by {self.user.username}"

    class Meta:
        verbose_name = "AI Request"
        verbose_name_plural = "AI Requests"
        ordering = ['-created_at']

class AITemplate(models.Model):
    TEMPLATE_CATEGORIES = [
        ('business', 'Business'),
        ('creative', 'Creative'),
        ('technical', 'Technical'),
        ('educational', 'Educational'),
        ('personal', 'Personal'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=TEMPLATE_CATEGORIES)
    prompt_template = models.TextField()
    variables = models.JSONField(default=list, blank=True)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    usage_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "AI Template"
        verbose_name_plural = "AI Templates"

class AIUsageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    tokens_consumed = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.ai_model.name} ({self.date})"

    class Meta:
        verbose_name = "AI Usage Log"
        verbose_name_plural = "AI Usage Logs"
        unique_together = ['user', 'ai_model', 'date']
