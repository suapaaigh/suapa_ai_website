from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
