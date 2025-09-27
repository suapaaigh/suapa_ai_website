from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path('', include('main.urls'))]
    urlpatterns += [path('accounts/', include('accounts.urls'))]
    urlpatterns += [path('copilot/', include('copilot.urls'))]
    urlpatterns += [path('bot/', include('bot.urls'))]
    urlpatterns += [path('aivi/', include('aivi.urls'))]
    urlpatterns += [path('companion/', include('companion.urls'))]
    urlpatterns += [path('chat/', include('chat.urls'))]