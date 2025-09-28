from django.shortcuts import render

# Create your views here.
def my_pilot(request):
    return render(request, 'chat/copilot.html')