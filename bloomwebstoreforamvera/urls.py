"""
URL configuration for bloomwebstoreforamvera project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path
from django.views.static import serve

from django.http import HttpResponse

def robots_txt(request):
    """
    Генерация robots.txt для соблюдения 149-ФЗ.
    Запрещаем индексацию всего сайта для защиты от автоматизированного сбора данных.
    """
    content = (
        "User-agent: *\n"
        "Disallow: /"
    )
    return HttpResponse(content, content_type="text/plain")




urlpatterns = [
    path('adminsimple1/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('shop.urls', namespace='shop')),
    path("robots.txt", robots_txt),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




if not settings.DEBUG:
    # Этот блок работает, когда DEBUG выключен (для Waitress и Amvera)
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
else:
    # Этот блок работает при разработке (стандартный способ)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)