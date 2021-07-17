from django.contrib.auth.decorators import login_required
from django.urls import path, include
from accounts.views import Login, logout, Register, Profile, changePassword, userOrders
from accounts import urls_reset

urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('register/', Register.as_view(), name="register"),
    path('logout/', logout, name="logout"),
    path('profile/', login_required(Profile.as_view()), name="profile"),
    path('password-reset/', include(urls_reset)),
    path('change_password/', login_required(changePassword.as_view()), name="change_password"),
    path('orders/', login_required(userOrders.as_view()), name="users_orders"),
]
