from django.urls import path
from .views import *

app_name = 'companion'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('my-companion/', my_companion, name='my-companion'),
]
