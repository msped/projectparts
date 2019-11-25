"""projectparts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path
from django.views import static
from .settings import MEDIA_ROOT

from home.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', home, name="home"),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^competition/', include('competition.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^tickets/', include('products.urls')),
    url(r'^checkout/', include('checkout.urls')),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': MEDIA_ROOT})
]
