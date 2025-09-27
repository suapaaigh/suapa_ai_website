from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Bot(models.Model):
    BOT_TYPES = [
        ('chatbot', 'Chatbot'),
        ('assistant', 'Assistant'),
        ('specialist', 'Specialist'),
        ('custom', 'Custom'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('training', 'Training'),
        ('maintenance', 'Maintenance'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    bot_type = models.CharField(max_length=20, choices=BOT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    system_prompt = models.TextField(blank=True)
    model_name = models.CharField(max_length=100, default='gpt-3.5-turbo')
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=1000)
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bot"
        verbose_name_plural = "Bots"

class BotConversation(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bot.name} conversation with {self.user.username}"

    class Meta:
        verbose_name = "Bot Conversation"
        verbose_name_plural = "Bot Conversations"
        ordering = ['-updated_at']

class BotMessage(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bot', 'Bot'),
        ('system', 'System'),
    ]

    conversation = models.ForeignKey(BotConversation, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    content = models.TextField()
    tokens_used = models.IntegerField(default=0)
    response_time = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.message_type.title()} message in {self.conversation}"

    class Meta:
        verbose_name = "Bot Message"
        verbose_name_plural = "Bot Messages"
        ordering = ['timestamp']

class BotKnowledgeBase(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='knowledge_base')
    title = models.CharField(max_length=200)
    content = models.TextField()
    source_url = models.URLField(blank=True)
    file_upload = models.FileField(upload_to='bot_knowledge/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bot.name} - {self.title}"

    class Meta:
        verbose_name = "Bot Knowledge Base"
        verbose_name_plural = "Bot Knowledge Bases"
