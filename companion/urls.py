from django.urls import path
from .views import *

urlpatterns = [
    path('my-companion/', my_companion, name='my-companion'),
]
