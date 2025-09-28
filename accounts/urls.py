from django.urls import path
from .views import *

urlpatterns = [
    # Authentication URLs
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('dashboard/', dashboard, name='dashboard'),

    # Password management
    path('password-change/', password_change, name='password-change'),
    path('password-reset/', password_reset_request, name='password-reset'),

    # Profile management
    path('profile-settings/', profile_settings, name='profile-settings'),
    path('content-recommendations/', content_recommendations, name='content-recommendations'),
]
