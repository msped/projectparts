from django.test import TestCase
from django.contrib.auth.models import User
from django import forms
from .forms import UserLoginForm, UserRegisterForm, UserDataForm, ProfileForm, ShippingForm

# Create your tests here.

class AccountFormsTests(TestCase):
    """Test all forms within the accounts app"""

    def setUp(self):
        user = User(
            username='test user',
            email='test@gmail.com',
            password='testpassword'
        )  
        user.save()

    def test_register_form_correct_data(self):
        """Test the register form with the correct data"""
        form = UserRegisterForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'test',
            'email': 'test@example.com',
            'password1': 'examplepassword',
            'password2': 'examplepassword',
        })
        self.assertTrue(form.is_valid())

    def test_register_form_incorrect_email_data(self):
        """Test the register form with the same email data"""
        form = UserRegisterForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'test',
            'email': 'test@gmail.com',
            'password1': 'examplepassword',
            'password2': 'examplepassword',
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Email address must be unique")

    def test_register_form_without_email(self):
        """Test the register form with the correct data"""
        form = UserRegisterForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'test',
            'email': '',
            'password1': 'examplepassword',
            'password2': 'examplepassword',
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Email address is required")

    def test_register_form_without_matching_passwords(self):
        """Test the register form with passwords that aren't matching"""
        form = UserRegisterForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'test',
            'email': 'test@example.com',
            'password1': 'examplepassword',
            'password2': 'examplepassword1',
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Passwords don't match")

    def test_login_form(self):
        """Test login form with correct data"""
        form = UserLoginForm({
            'username': 'test@gmail.com',
            'password': 'testpassword'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_no_email(self):
        """Test for the login form without an email"""
        form = UserLoginForm({
            'username': '',
            'password': 'testpassword'
        })
        self.assertFalse(form.is_valid())

    def test_login_form_no_password(self):
        """Test for the login form without a password"""
        form = UserLoginForm({
            'username': 'test@gmail.com',
            'password': ''
        })
        self.assertFalse(form.is_valid())

    def test_user_data_form(self):
        """Test UserDataForm with correct data"""
        form = UserDataForm({
            'first_name': 'Joe',
            'last_name': 'Bloggs',
            'email': 'test@hotmail.co.uk'
        })
        self.assertTrue(form.is_valid())

    def test_user_data_form_no_first_name(self):
        """Test UserDataForm without first name"""
        form = UserDataForm({
            'first_name': '',
            'last_name': 'Bloggs',
            'email': 'test@hotmail.co.uk'
        })
        self.assertFalse(form.is_valid())

    def test_user_data_form_no_last_name(self):
        """Test UserDataForm without last name"""
        form = UserDataForm({
            'first_name': 'Joe',
            'last_name': '',
            'email': 'test@hotmail.co.uk'
        })
        self.assertFalse(form.is_valid())

    def test_user_data_form_no_email(self):
        """Test UserDataForm without email"""
        form = UserDataForm({
            'first_name': 'Joe',
            'last_name': 'Bloggs',
            'email': ''
        })
        self.assertFalse(form.is_valid())

    def test_user_data_form_invalid_email(self):
        """Test UserDataForm with invalid email"""
        form = UserDataForm({
            'first_name': 'Joe',
            'last_name': 'Bloggs',
            'email': 'testmail.com'
        })
        self.assertFalse(form.is_valid())

    def test_profile_form(self):
        """Test profile form"""
        form = ProfileForm({
            'phone_number': '07894461574'
        })
        self.assertTrue(form.is_valid())

    def test_profile_form_without_data(self):
        """Test profile form without data"""
        form = ProfileForm({
            'phone_number': ''
        })
        self.assertFalse(form.is_valid())

    def test_shipping_form(self):
        """Test ShippingForm with correct data"""
        form = ShippingForm({
            'address_line_1': '3 Rosewood Drive',
            'address_line_2': '',
            'town_city': 'Winsford',
            'county': 'Cheshire',
            'country': 'UK',
            'postcode': 'CW7 6AO'
        })
        self.assertTrue(form.is_valid())

    def test_shipping_form_without_required_data(self):
        """Test ShippingForm without data"""
        form = ShippingForm({
            'address_line_1': '3 Rosewood Drive',
            'address_line_2': '',
            'town_city': 'Winsford',
            'county': '',
            'country': '',
            'postcode': 'CW7 6AO'
        })
        self.assertFalse(form.is_valid())
