from django.shortcuts import render

# Create your views here.
def my_companion(request):
    return render(request, 'chat/companion.html')