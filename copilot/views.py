from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def my_pilot(request):
    return render(request, 'chat/copilot.html')

@login_required
def dashboard(request):
    """Copilot dashboard"""
    page_name = "Code Assistant"

    context = {
        'page_name': page_name
    }
    return render(request, 'chat/copilot.html', context)