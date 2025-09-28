"""
Authentication middleware for SUA PA AI
"""

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin

class AuthenticationMiddleware(MiddlewareMixin):
    """
    Custom authentication middleware to handle redirects and user flow
    """

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self, request):
        """
        Process requests before they reach the view
        """
        # Skip processing for admin, static files, and authentication URLs
        if (request.path.startswith('/admin/') or
            request.path.startswith('/static/') or
            request.path.startswith('/media/') or
            request.path.startswith('/accounts/signin/') or
            request.path.startswith('/accounts/signup/') or
            request.path.startswith('/accounts/password-reset/')):
            return None

        # If user is authenticated but tries to access signin/signup
        if request.user.is_authenticated:
            if request.path in ['/accounts/signin/', '/accounts/signup/']:
                messages.info(request, 'You are already signed in.')
                return redirect('dashboard')

        return None

class ProfileCompletionMiddleware(MiddlewareMixin):
    """
    Middleware to ensure user profiles are completed
    """

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self, request):
        """
        Check if authenticated users have completed their profiles
        """
        # Skip for non-authenticated users and exempt URLs
        if not request.user.is_authenticated:
            return None

        # Exempt URLs that don't require profile completion
        exempt_urls = [
            '/admin/',
            '/accounts/signout/',
            '/accounts/profile-settings/',
            '/accounts/password-change/',
            '/static/',
            '/media/',
        ]

        if any(request.path.startswith(url) for url in exempt_urls):
            return None

        # Check if user has completed profile
        try:
            profile = request.user.userprofile
            if not profile.onboarding_completed and request.path != '/accounts/profile-settings/':
                messages.info(request, 'Please complete your profile setup to continue.')
                return redirect('profile-settings')
        except:
            # Profile doesn't exist, create one and redirect to settings
            from .models import UserProfile
            UserProfile.objects.create(user=request.user)
            messages.info(request, 'Please complete your profile setup.')
            return redirect('profile-settings')

        return None

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to responses
    """

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        response = self.get_response(request)

        # Add security headers
        if not response.get('X-Content-Type-Options'):
            response['X-Content-Type-Options'] = 'nosniff'

        if not response.get('X-Frame-Options'):
            response['X-Frame-Options'] = 'DENY'

        if not response.get('X-XSS-Protection'):
            response['X-XSS-Protection'] = '1; mode=block'

        return response