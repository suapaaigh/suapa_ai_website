from django.contrib import admin
from .models import AIModel, AIRequest, AITemplate, AIUsageLog

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'provider', 'is_active', 'cost_per_token', 'created_at']
    list_filter = ['model_type', 'provider', 'is_active', 'requires_api_key']
    search_fields = ['name', 'description', 'provider', 'model_id']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Model Information', {
            'fields': ('name', 'description', 'model_type', 'provider')
        }),
        ('Technical Details', {
            'fields': ('model_id', 'api_endpoint', 'max_tokens', 'requires_api_key')
        }),
        ('Pricing', {
            'fields': ('cost_per_token',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ai_model', 'request_type', 'status', 'tokens_used', 'cost', 'created_at']
    list_filter = ['request_type', 'status', 'ai_model__name', 'created_at']
    search_fields = ['user__username', 'ai_model__name', 'prompt']
    readonly_fields = ['created_at', 'completed_at']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'ai_model', 'request_type', 'status')
        }),
        ('Content', {
            'fields': ('prompt', 'response', 'error_message')
        }),
        ('Metrics', {
            'fields': ('tokens_used', 'processing_time', 'cost')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        })
    )

@admin.register(AITemplate)
class AITemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'ai_model', 'is_public', 'usage_count', 'created_by', 'created_at']
    list_filter = ['category', 'ai_model__name', 'is_public', 'created_at']
    search_fields = ['name', 'description', 'created_by__username']
    readonly_fields = ['usage_count', 'created_at', 'updated_at']
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'description', 'category', 'ai_model')
        }),
        ('Template Content', {
            'fields': ('prompt_template', 'variables')
        }),
        ('Settings', {
            'fields': ('is_public', 'created_by')
        }),
        ('Statistics', {
            'fields': ('usage_count',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(AIUsageLog)
class AIUsageLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'ai_model', 'tokens_consumed', 'cost', 'date']
    list_filter = ['ai_model__name', 'date']
    search_fields = ['user__username', 'ai_model__name']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
