from django.shortcuts import render

# Create your views here.
def chat(request):
    page_name = "Chat"

    context = {
        'page_name':page_name
    }
    return render(request, 'chat.html', context)