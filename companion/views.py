from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def my_companion(request):
    return render(request, 'chat/companion.html')

@login_required
def dashboard(request):
    """Companion dashboard"""
    page_name = "Study Companion"

    context = {
        'page_name': page_name
    }
    return render(request, 'chat/companion.html', context)