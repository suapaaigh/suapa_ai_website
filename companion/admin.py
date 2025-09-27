from django.contrib import admin
from .models import CompanionPersonality, Companion, CompanionConversation, CompanionMessage, CompanionMemory

class CompanionMemoryInline(admin.TabularInline):
    model = CompanionMemory
    extra = 0
    readonly_fields = ['last_accessed', 'access_count', 'created_at']

class CompanionMessageInline(admin.TabularInline):
    model = CompanionMessage
    extra = 0
    readonly_fields = ['timestamp']
    fields = ['message_type', 'content', 'emotion', 'timestamp']

@admin.register(CompanionPersonality)
class CompanionPersonalityAdmin(admin.ModelAdmin):
    list_display = ['name', 'personality_type', 'is_active', 'created_at']
    list_filter = ['personality_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'personality_type', 'avatar')
        }),
        ('Configuration', {
            'fields': ('traits', 'system_prompt')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Companion)
class CompanionAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'personality', 'status', 'learning_enabled', 'memory_enabled', 'created_at']
    list_filter = ['personality__name', 'status', 'learning_enabled', 'memory_enabled', 'created_at']
    search_fields = ['name', 'user__username', 'personality__name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CompanionMemoryInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'personality', 'status')
        }),
        ('Configuration', {
            'fields': ('custom_instructions', 'learning_enabled', 'memory_enabled')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CompanionConversation)
class CompanionConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'companion', 'title', 'topic', 'mood', 'is_active', 'created_at']
    list_filter = ['is_active', 'mood', 'created_at']
    search_fields = ['companion__name', 'companion__user__username', 'title', 'topic']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CompanionMessageInline]
    date_hierarchy = 'created_at'

@admin.register(CompanionMessage)
class CompanionMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'message_type', 'content_preview', 'emotion', 'timestamp']
    list_filter = ['message_type', 'emotion', 'timestamp']
    search_fields = ['conversation__companion__name', 'content']
    readonly_fields = ['timestamp']

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(CompanionMemory)
class CompanionMemoryAdmin(admin.ModelAdmin):
    list_display = ['companion', 'memory_type', 'content_preview', 'importance', 'access_count', 'last_accessed']
    list_filter = ['memory_type', 'importance', 'created_at']
    search_fields = ['companion__name', 'companion__user__username', 'content']
    readonly_fields = ['last_accessed', 'access_count', 'created_at']

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'
