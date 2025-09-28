from django.urls import path
from .views import *

urlpatterns = [
    path('my-bot', my_bot, name='my-bot'),
]
