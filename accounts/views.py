from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import UserLoginForm, UserRegisterForm, UserDataForm, ProfileForm, ShippingForm

def login(request):
    """Logs a user in / display login page"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in.")
                return redirect('home')
            else:
                login_form.add_error(None, "Your email or password are incorrect")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})

@login_required
def logout(request):
    """Log user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out.")
    return redirect(reverse('login'))

def register(request):
    """register user"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered.")
                return redirect('home')
            else:
                messages.error(request, "Unable to register account.")
    else:
        register_form = UserRegisterForm()

    return render(request, 'register.html', {'register_form': register_form})

@login_required
def profilepage(request):
    """Displays Profile Page / Handles updating of profile"""
    if request.method == 'POST':
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
    else:
        user = User.objects.filter(id=request.user.id).first()
        if user.profile.phone_number == '':
            user_form = UserDataForm(instance=request.user)
            profile_form = ProfileForm()
            shipping_form = ShippingForm()
        else:
            user_form = UserDataForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
            shipping_form = ShippingForm(instance=request.user.profile)

    forms = {
        'UserDataForm': user_form,
        'ProfileForm': profile_form,
        'Shippingform': shipping_form
    }
    return render(request, 'profile.html', forms)

@login_required
def change_password(request):
    """Displays Change Password Page / Changes password in DB"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password has been updated')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'change_password_form': form})
