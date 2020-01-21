from django import forms
from django.core.validators import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserLoginForm(forms.Form):
    """Form to log a user in"""
    username = forms.CharField(label="E-mail")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['E-mail', 'Password']

class UserRegisterForm(UserCreationForm):
    """Form for registering a new user"""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]

    def clean_email(self):
        """checks if email is already in use"""
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email == '':
            raise forms.ValidationError(u'Email address is required')
        elif User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email address must be unique')
        return email

    def clean_password2(self):
        """Checks is password match"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Please confirm your password")

        if password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2

class UserDataForm(forms.ModelForm):
    """To change first name, last name, email and phone number"""
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    """To change user phone number"""
    phone_number = forms.CharField(max_length=11)

    class Meta:
        model = Profile
        fields = ['phone_number']

class ShippingForm(forms.ModelForm):
    """To change billing / shipping form"""
    address_line_1 = forms.CharField(max_length=40)
    address_line_2 = forms.CharField(max_length=40, required=False)
    town_city = forms.CharField(max_length=40)
    county = forms.CharField(max_length=40)
    country = forms.CharField(max_length=40)
    postcode = forms.CharField(max_length=10)

    class Meta:
        model = Profile
        fields = [
            'address_line_1',
            'address_line_2',
            'town_city',
            'county',
            'country',
            'postcode'
        ]
