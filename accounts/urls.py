from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('profile-settings/', profile_settings, name='profile-settings'),
    path('content-recommendations/', content_recommendations, name='content-recommendations'),
]
