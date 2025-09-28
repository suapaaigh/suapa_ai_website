from django.urls import path
from .views import *

app_name = 'copilot'

urlpatterns = [
    path('my-pilot/', my_pilot, name='my-pilot'),
]
