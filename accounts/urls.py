from django.conf.urls import url, include
from accounts.views import login, logout, register, profilepage, change_password
from accounts import urls_reset

urlpatterns = [
    url(r'^login/', login, name="login"),
    url(r'^register/', register, name="register"),
    url(r'^logout/', logout, name="logout"),
    url(r'^profile/', profilepage, name="profile"),
    url(r'^password-reset/', include(urls_reset)),
    url(r'^change_password/', change_password, name="change_password"),
]