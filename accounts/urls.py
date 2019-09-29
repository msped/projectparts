from django.conf.urls import url, include
from accounts.views import login, logout, register

urlpatterns = [
    url(r'^login/', login, name="login"),
    url(r'^register/', register, name="register"),
    url(r'^logout/', logout, name="logout"),
]