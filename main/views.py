from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import *

# Create your views here.
def home(request):
    hero = Hero.objects.first()
    why = WhyChooseUs.objects.all()
    features = Feature.objects.all()
    featured_image = FeaturedImage.objects.first()
    testimonials = Testimonial.objects.all()
    blogs = BlogPost.objects.filter(is_featured = True).all()
    products = Product.objects.filter(is_active=True).order_by('order', 'name')

    context = {
        'hero':hero,
        'why':why,
        'features':features,
        'featured_image':featured_image,
        'testimonials':testimonials,
        'blogs':blogs,
        'products':products
    }
    return render(request, 'index.html', context)


def about_us(request):
    page_name = "About Us"
    about_us = AboutUs.objects.first()
    faq = FAQ.objects.all()
    blogs = BlogPost.objects.filter(is_featured = True).all()

    context = {
        'page_name':page_name,
        'about_us':about_us,
        'faqs':faq,
        'blogs':blogs,
    }
    return render(request, 'about.html', context)


def blogs(request):
    page_name = "Our Blog"
    blogs = BlogPost.objects.all()

    context = {
        'page_name':page_name,
        'blogs':blogs
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
    faqs = FAQ.objects.all()

    context = {
        'page_name':page_name,
        'faqs':faqs
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
    products = Product.objects.filter(is_active=True).order_by('order', 'name')

    context = {
        'page_name':page_name,
        'products':products
    }
    return render(request, 'price.html', context)


def single_blog(request, slug):
    blog = BlogPost.objects.get(slug=slug)
    categories_with_counts = Category.objects.annotate(post_count=Count('posts')).all()

    # Get recent posts from the last week
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_posts = BlogPost.objects.filter(
        published_at__gte=one_week_ago,
        status='published'
    ).exclude(id=blog.id).order_by('-published_at')[:5]

    # Get active products for pricing table
    products = Product.objects.filter(is_active=True).order_by('order', 'name')

    page_name = blog

    context = {
        'blog':blog,
        'page_name':page_name,
        'categories':categories_with_counts,
        'recent_posts':recent_posts,
        'products':products
    }
    return render(request, 'blog-details.html', context)


def services(request):
    page_name = "Our Services"

    context = {
        'page_name':page_name
    }
    return render(request, 'service.html', context)


def team(request):
    page_name = "Our Team"
    team_members = TeamMember.objects.filter()
    ceo = TeamMember.objects.filter(position__icontains = 'CEO').first()

    context = {
        'page_name':page_name,
        'team_members':team_members,
        'ceo':ceo
    }
    return render(request, 'team.html', context)
