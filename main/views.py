from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')


def about_us(request):
    page_name = "About Us"

    context = {
        'page_name':page_name
    }
    return render(request, 'about.html', context)


def blogs(request):
    return render(request, 'blog.html')


def contact(request):
    return render(request, 'contact.html')


def downloads(request):
    return render(request, 'shop.html')


def faq(request):
    return render(request, 'faq.html')


def portfolio(request):
    return render(request, 'work.html')



def pricing(request):
    return render(request, 'price.html')


def single_blog(request):
    return render(request, 'blog-details.html')


def services(request):
    return render(request, 'service.html')


def team(request):
    return render(request, 'team.html')
