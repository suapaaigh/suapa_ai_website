from django.shortcuts import render

# Create your views here.
def signup(request):
    page_name = "Sign Up"

    context = {
        'page_name':page_name
    }
    return render(request, 'signup.html', context)


def signin(request):
    page_name = "Sign In"

    context = {
        'page_name':page_name
    }
    return render(request, 'signin.html', context)