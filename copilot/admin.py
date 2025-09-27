from django.contrib import admin
from .models import CopilotProject, CopilotSession, CopilotInteraction, CopilotCodeSuggestion, CopilotLearningProgress

class CopilotSessionInline(admin.TabularInline):
    model = CopilotSession
    extra = 0
    readonly_fields = ['started_at', 'ended_at']

class CopilotInteractionInline(admin.TabularInline):
    model = CopilotInteraction
    extra = 0
    readonly_fields = ['timestamp']
    fields = ['interaction_type', 'user_input', 'was_helpful', 'timestamp']

@admin.register(CopilotProject)
class CopilotProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'project_type', 'status', 'programming_language', 'framework', 'created_at']
    list_filter = ['project_type', 'status', 'programming_language', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CopilotSessionInline]
    fieldsets = (
        ('Project Information', {
            'fields': ('user', 'name', 'description', 'project_type', 'status')
        }),
        ('Technical Details', {
            'fields': ('programming_language', 'framework', 'repository_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CopilotSession)
class CopilotSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'session_type', 'title', 'is_active', 'started_at', 'ended_at']
    list_filter = ['session_type', 'is_active', 'started_at']
    search_fields = ['project__name', 'title', 'goal']
    readonly_fields = ['started_at', 'ended_at']
    inlines = [CopilotInteractionInline]
    date_hierarchy = 'started_at'

@admin.register(CopilotInteraction)
class CopilotInteractionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'interaction_type', 'user_input_preview', 'was_helpful', 'timestamp']
    list_filter = ['interaction_type', 'was_helpful', 'timestamp']
    search_fields = ['session__project__name', 'user_input', 'copilot_response']
    readonly_fields = ['timestamp']

    def user_input_preview(self, obj):
        return obj.user_input[:100] + '...' if len(obj.user_input) > 100 else obj.user_input
    user_input_preview.short_description = 'User Input Preview'

@admin.register(CopilotCodeSuggestion)
class CopilotCodeSuggestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'status', 'confidence_score', 'file_path', 'created_at']
    list_filter = ['status', 'confidence_score', 'created_at']
    search_fields = ['session__project__name', 'file_path', 'suggested_code']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Suggestion Information', {
            'fields': ('session', 'status', 'confidence_score')
        }),
        ('Code Details', {
            'fields': ('original_code', 'suggested_code', 'explanation')
        }),
        ('File Information', {
            'fields': ('file_path', 'start_line', 'end_line')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CopilotLearningProgress)
class CopilotLearningProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'technology', 'skill_level', 'progress_percentage', 'last_practice_date']
    list_filter = ['skill_level', 'technology', 'last_practice_date']
    search_fields = ['user__username', 'technology']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'technology', 'skill_level')
        }),
        ('Progress Details', {
            'fields': ('progress_percentage', 'topics_completed', 'last_practice_date', 'total_practice_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
