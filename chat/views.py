from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def chat(request):
    page_name = "Chat"

    context = {
        'page_name': page_name
    }
    return render(request, 'chat/chat.html', context)

@login_required
def index(request):
    """Main chat index page"""
    page_name = "AI Chat"

    context = {
        'page_name': page_name
    }
    return render(request, 'chat/index.html', context)