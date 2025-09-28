from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def my_bot(request):
    page_name = "Sua Pa AI Bot"

    context = {
        'page_name':page_name
    }
    return render(request, 'chat/bot.html', context)