from django.contrib import admin
from .models import (
    CompanionPersonality, Companion, CompanionConversation, CompanionMessage, CompanionMemory,
    KnowledgeArea, SubjectContent, UserLearningProgress
)

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

@admin.register(KnowledgeArea)
class KnowledgeAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'education_level', 'subject_category', 'difficulty_level', 'is_active', 'created_at']
    list_filter = ['education_level', 'subject_category', 'difficulty_level', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'curriculum_code']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['prerequisites']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'education_level', 'subject_category')
        }),
        ('Grade Configuration', {
            'fields': ('grade_levels', 'curriculum_code', 'prerequisites')
        }),
        ('Content', {
            'fields': ('learning_objectives', 'assessment_criteria', 'topics', 'skills_developed')
        }),
        ('Settings', {
            'fields': ('difficulty_level', 'estimated_hours', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

class SubjectContentInline(admin.TabularInline):
    model = SubjectContent
    extra = 0
    fields = ['title', 'content_type', 'difficulty_level', 'order_index', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SubjectContent)
class SubjectContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'knowledge_area', 'content_type', 'difficulty_level', 'order_index', 'success_rate', 'is_active']
    list_filter = ['knowledge_area__education_level', 'content_type', 'difficulty_level', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'knowledge_area__name']
    readonly_fields = ['created_at', 'updated_at', 'success_rate', 'engagement_score']
    fieldsets = (
        ('Basic Information', {
            'fields': ('knowledge_area', 'title', 'description', 'content_type', 'difficulty_level')
        }),
        ('Content Details', {
            'fields': ('content_data', 'duration_minutes', 'order_index')
        }),
        ('Learning Outcomes', {
            'fields': ('learning_outcomes', 'tags')
        }),
        ('Analytics', {
            'fields': ('success_rate', 'engagement_score'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(UserLearningProgress)
class UserLearningProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'knowledge_area', 'content', 'status', 'progress_percentage', 'best_score', 'last_accessed']
    list_filter = ['status', 'knowledge_area__education_level', 'knowledge_area__name', 'created_at']
    search_fields = ['user__username', 'user__email', 'knowledge_area__name', 'content__title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'last_accessed'
    fieldsets = (
        ('User & Content', {
            'fields': ('user', 'knowledge_area', 'content', 'status')
        }),
        ('Progress Metrics', {
            'fields': ('progress_percentage', 'attempts', 'best_score', 'average_score', 'time_spent_minutes')
        }),
        ('Adaptive Learning', {
            'fields': ('difficulty_adjustment', 'mastery_level', 'last_accessed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
