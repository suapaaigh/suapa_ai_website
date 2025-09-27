from django.contrib import admin
from .models import (
    Category, Tag, BlogPost, Service, TeamMember, Portfolio, FAQ, ContactMessage,
    Hero, WhyChooseUs, Feature, Partner, Testimonial, AboutUs, FeaturedImage
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    readonly_fields = ['slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views', 'created_at', 'published_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['slug', 'views', 'created_at', 'updated_at', 'published_at']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'published_at'
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        ('Organization', {
            'fields': ('category', 'tags', 'author')
        }),
        ('Publication', {
            'fields': ('status', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('views',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_description', 'price', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description', 'short_description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'name']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'email', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'position', 'bio', 'email']
    readonly_fields = ['created_at']
    ordering = ['order', 'name']

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_type', 'client', 'is_featured', 'completed_date', 'created_at']
    list_filter = ['project_type', 'is_featured', 'completed_date', 'created_at']
    search_fields = ['title', 'description', 'client']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'completed_date'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active', 'order']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'category']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'question']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject', 'status')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ['caption', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['caption', 'welcome_text']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', '-created_at']
    fieldsets = (
        ('Content', {
            'fields': ('caption', 'welcome_text', 'hero_image')
        }),
        ('Call to Action', {
            'fields': ('button_text', 'button_url')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ['caption', 'why_image', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['caption', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'caption']

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['caption', 'icon', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['caption', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'caption']

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'website_url', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'name']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'company', 'rating', 'is_featured', 'is_active', 'order']
    list_filter = ['is_featured', 'is_active', 'rating', 'created_at']
    search_fields = ['name', 'position', 'company', 'testimony']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', '-created_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'position', 'company', 'profile_image')
        }),
        ('Testimonial', {
            'fields': ('testimony', 'rating')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'years_of_experience', 'projects_completed', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Company Values', {
            'fields': ('mission', 'vision', 'values')
        }),
        ('Images', {
            'fields': ('main_image', 'secondary_image')
        }),
        ('Statistics', {
            'fields': ('years_of_experience', 'projects_completed', 'happy_clients', 'team_members')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(FeaturedImage)
class FeaturedImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'usage', 'is_active', 'order', 'created_at']
    list_filter = ['usage', 'is_active', 'created_at']
    search_fields = ['title', 'alt_text', 'caption']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['usage', 'order', '-created_at']
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'image', 'alt_text', 'caption')
        }),
        ('Usage & Settings', {
            'fields': ('usage', 'link_url', 'is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
