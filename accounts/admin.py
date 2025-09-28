from django.contrib import admin
from .models import UserProfile, Subscription, UserEducationProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_premium', 'premium_expiry', 'created_at']
    list_filter = ['is_premium', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'avatar', 'bio')
        }),
        ('Contact Details', {
            'fields': ('phone_number', 'date_of_birth', 'location', 'website')
        }),
        ('Premium Status', {
            'fields': ('is_premium', 'premium_expiry')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew']
    list_filter = ['plan', 'status', 'auto_renew', 'start_date']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'

@admin.register(UserEducationProfile)
class UserEducationProfileAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'learning_pace', 'motivation_type', 'overall_performance', 'created_at']
    list_filter = ['learning_pace', 'motivation_type', 'created_at']
    search_fields = ['user_profile__user__username', 'user_profile__user__email']
    readonly_fields = ['created_at', 'updated_at', 'overall_performance', 'improvement_rate', 'consistency_score']
    filter_horizontal = ['favorite_subjects', 'strong_subjects', 'weak_subjects']
    fieldsets = (
        ('Learning Behavior', {
            'fields': ('user_profile', 'learning_pace', 'motivation_type', 'average_study_session')
        }),
        ('Subject Preferences', {
            'fields': ('favorite_subjects', 'strong_subjects', 'weak_subjects')
        }),
        ('Content Preferences', {
            'fields': ('preferred_content_types',)
        }),
        ('Accessibility', {
            'fields': ('accessibility_needs', 'special_considerations')
        }),
        ('Performance Metrics', {
            'fields': ('overall_performance', 'improvement_rate', 'consistency_score'),
            'classes': ('collapse',)
        }),
        ('Adaptive Learning', {
            'fields': ('difficulty_adaptation', 'content_recommendation_weights'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
