from django.conf.urls import url
from .views import contact_view

urlpatterns = [
    url(r'^$', contact_view, name="contact"),
]