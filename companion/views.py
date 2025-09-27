from django.shortcuts import render

# Create your views here.
def assistance(request):
    return render(request, 'companion.html')