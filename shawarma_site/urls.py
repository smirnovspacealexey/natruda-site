"""shawarma_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.urls import path
from apps.signboard.urls import urlpatterns as urlpatterns_signboard
from apps.main.views import menu_pdf, menu_pictures
from apps.sber.urls import urlpatterns as urlpatterns_sber
from apps.main.views import counter

urlpatterns = [
    path('', counter, name='counter'),
    url(r'^customer_interface/', include('customer_interface.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^menu-pdf/', menu_pdf),
    url(r'^menu/', menu_pictures),
]

urlpatterns += urlpatterns_signboard
urlpatterns += urlpatterns_sber
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
