from django.urls import path
from .views import *

urlpatterns = [
    path('assistance/', assistance, name='assistance'),
]
