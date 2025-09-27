from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('about-us/', about_us, name='about-us'),
    path('blog/', blogs, name='blogs'),
    path('contact/', contact, name='contact'),
    path('downloads/', downloads, name='downloads'),
    path('faq/', faq, name='faq'),
    path('portfolio/', portfolio, name='portfolio'),
    path('pricing/', pricing, name='pricing'),
    path('single-blog/', single_blog, name='single-blog'),
    path('services/', services, name='services'),
    path('team/', team, name='team'),
]
