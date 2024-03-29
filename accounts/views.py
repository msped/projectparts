from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from accounts.forms import (
    UserLoginForm,
    UserRegisterForm,
    UserDataForm,
    ProfileForm,
    ShippingForm
)
from cart.models import Order
from .utils import add_session_items_to_db, get_users_orders

class Login(View):
    """Logs user in / creates user account
    or redirect user to home if already logged in"""
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            login_form = UserLoginForm()
        return render(request, self.template_name, {'login_form': login_form})  

    def post(self, request):
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                add_session_items_to_db(request)
                messages.success(request, "You have successfully logged in.")
                return redirect('home')
            else:
                login_form.add_error(
                    None,
                    "Your email or password are incorrect"
                )
        return render(request, self.template_name, {'login_form': login_form})

@login_required
def logout(request):
    """Log user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out.")
    return redirect(reverse('login'))        

class Register(View):
    """Register page / registers user or redirects 
    user to home if already logged in"""
    template_name = 'register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            register_form = UserRegisterForm()
        return render(request, self.template_name, {'register_form': register_form})

    def post(self, request):
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                add_session_items_to_db(request)
                messages.success(request, "You have successfully registered.")
                return redirect('home')
            else:
                messages.error(request, "Unable to register account.")

        return render(request, self.template_name, {'register_form': register_form})

class Profile(View):
    template_name = 'profile.html'
    
    def get(self, request):
        user_form = UserDataForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        shipping_form = ShippingForm(instance=request.user.profile)

        forms = {
            'UserDataForm': user_form,
            'ProfileForm': profile_form,
            'Shippingform': shipping_form
        }
        return render(request, self.template_name, forms)

    def post(self, request):
        if 'user-information' in request.POST:
            user_form = UserDataForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST,
                                       instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "User Information Updated.")
                return redirect('profile')
        else:
            shipping_form = ShippingForm(request.POST,
                                         instance=request.user.profile)
            if shipping_form.is_valid():
                shipping_form.save()
                messages.success(request, "User Information Updated.")
                return redirect('profile')

class changePassword(View):
    """Displays Change Password Page / Changes password in DB"""
    template_name = 'change_password.html'

    def get(self, request):
        form = PasswordChangeForm(request.user)
        context = {'change_password_form': form}
        return render(request,self.template_name, context)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password has been updated')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('change_password')

class userOrders(View):
    """View for a user to view all orders that are made"""
    template_name = 'users_orders.html'

    def get(self, request):
        try:
            orders = Order.objects.filter(
                user=request.user.id
            ).order_by('-id')
        except Order.DoesNotExist:
            return render(request, 'users_orders.html', {
                'users_orders': False
            })

        all_users_orders = get_users_orders(orders)
        paginator = Paginator(all_users_orders, 15)
        page = request.GET.get('page')
        user_orders = paginator.get_page(page)

        content = {
            'users_orders': user_orders
        }
        return render(request, self.template_name, content)

