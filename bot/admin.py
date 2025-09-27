from django.contrib import admin
from .models import Bot, BotConversation, BotMessage, BotKnowledgeBase

class BotKnowledgeBaseInline(admin.TabularInline):
    model = BotKnowledgeBase
    extra = 0
    readonly_fields = ['created_at', 'updated_at']

class BotMessageInline(admin.TabularInline):
    model = BotMessage
    extra = 0
    readonly_fields = ['timestamp']
    fields = ['message_type', 'content', 'tokens_used', 'response_time', 'timestamp']

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ['name', 'bot_type', 'status', 'is_public', 'created_by', 'created_at']
    list_filter = ['bot_type', 'status', 'is_public', 'created_at']
    search_fields = ['name', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [BotKnowledgeBaseInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'bot_type', 'status', 'created_by')
        }),
        ('AI Configuration', {
            'fields': ('system_prompt', 'model_name', 'temperature', 'max_tokens')
        }),
        ('Visibility', {
            'fields': ('is_public',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(BotConversation)
class BotConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'bot', 'user', 'title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'bot__name']
    search_fields = ['bot__name', 'user__username', 'title']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [BotMessageInline]
    date_hierarchy = 'created_at'

@admin.register(BotMessage)
class BotMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'message_type', 'content_preview', 'tokens_used', 'response_time', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['conversation__bot__name', 'conversation__user__username', 'content']
    readonly_fields = ['timestamp']

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(BotKnowledgeBase)
class BotKnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'bot', 'is_active', 'source_url', 'created_at']
    list_filter = ['is_active', 'created_at', 'bot__name']
    search_fields = ['title', 'content', 'bot__name']
    readonly_fields = ['created_at', 'updated_at']
