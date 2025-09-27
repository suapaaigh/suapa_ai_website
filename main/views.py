from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    hero = Hero.objects.first()
    why = WhyChooseUs.objects.all()

    context = {
        'hero':hero,
        'why':why,
    }
    return render(request, 'index.html', context)


def about_us(request):
    page_name = "About Us"

    context = {
        'page_name':page_name
    }
    return render(request, 'about.html', context)


def blogs(request):
    page_name = "Our Blog"

    context = {
        'page_name':page_name
    }
    return render(request, 'blog.html', context)


def contact(request):
    page_name = "Contact Us"

    context = {
        'page_name':page_name
    }
    return render(request, 'contact.html', context)


def downloads(request):
    page_name = "Downloads"

    context = {
        'page_name':page_name
    }
    return render(request, 'shop.html', context)


def faq(request):
    page_name = "FAQ"

    context = {
        'page_name':page_name
    }
    return render(request, 'faq.html', context)


def portfolio(request):
    page_name = "Our Portfolio"

    context = {
        'page_name':page_name
    }
    return render(request, 'work.html', context)



def pricing(request):
    page_name = "Our Pricing"

    context = {
        'page_name':page_name
    }
    return render(request, 'price.html', context)


def single_blog(request):
    return render(request, 'blog-details.html')


def services(request):
    page_name = "Our Services"

    context = {
        'page_name':page_name
    }
    return render(request, 'service.html', context)


def team(request):
    page_name = "Our Team"

    context = {
        'page_name':page_name
    }
    return render(request, 'team.html', context)
