from django.urls import path
from .views import *


urlpatterns = [
    path('my-pilot/', my_pilot, name='my-pilot'),
]
