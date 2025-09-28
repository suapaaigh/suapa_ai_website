from django.shortcuts import render

# Create your views here.
def my_bot(request):
    page_name = "Sua Pa AI Bot"

    context = {
        'page_name':page_name
    }
    return render(request, 'chat/bot.html', context)