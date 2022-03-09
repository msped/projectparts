from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from django import forms
from competition.models import Competition
from products.models import Product, Manufacturer, Categories
from cart.models import Order, OrderItem
from checkout.models import Entries
from .forms import UserLoginForm, UserRegisterForm, UserDataForm, ProfileForm, ShippingForm
from .apps import AccountsConfig
from .utils import get_users_orders

# Create your tests here.

class AccountViewsTest(TestCase):
    """Test for Account Views"""

    def setUp(self):
        self.user = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': 'test user',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        self.user2 = {
            'username': 'test user 2',
            'email': 'test2@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)
        User.objects.create_user(**self.user2)

        Competition(is_active=True).save()

    def test_login_page_response(self):
        """Test response of login page when not logged in"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_response_logged_in(self):
        """test response of the login age if the user is logged in
        should redirect (302 response)"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/accounts/login/', follow=True)
        self.assertIn(
            b'<h1 class="display-4">Welcome to Project Parts</h1>',
            response.content
        )

    def test_login_with_inccorect_details(self):
        """Test login with incorrect details"""
        response = self.client.post(
            '/accounts/login/',
            {
                'username': 'notanaccount@example.com',
                'password': 'examplepassword'
            },
            follow=True
        )
        self.assertIn(b'Your email or password are incorrect', response.content)

    def test_profile_page_response_user_not_logged_in(self):
        """Test where the profile page should return to login page if
        no user logged in"""
        response = self.client.get('/accounts/profile/', follow=True)
        self.assertIn(b'<h1>Login</h1>', response.content)

    def test_profile_page_response_user_logged_in(self):
        """Test page response when user is logged in"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/accounts/profile/', follow=True)
        self.assertIn(b'<h1>Profile</h1>', response.content)
        self.assertIn(
            b'<input type="text" name="first_name" value="John" class=" form-control" required id="id_first_name">',
            response.content
        )
        self.assertIn(
            b'<input type="text" name="last_name" value="Smith" class=" form-control" required id="id_last_name">',
            response.content
        )
        self.assertIn(
            b'<input type="email" name="email" value="test@gmail.com" class=" form-control" required id="id_email">',
            response.content
        )

    def test_logout_when_user_logged_in(self):
        """Test logout function"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertIn(b'<h1>Login</h1>', response.content)

    def test_logout_when_logged_out(self):
        """Test where the logout view should return to login page if
        no user logged in"""
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertIn(b'<h1>Login</h1>', response.content)

    def test_change_password_when_user_logged_in(self):
        """Test change password when a user is logged in"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/accounts/change_password/', follow=True)
        self.assertIn(b'<h1>Change Password</h1>', response.content)

    def test_change_password_when_user_logged_out(self):
        """Test where the change passowrd should return to login page if
        no user logged in"""
        response = self.client.get('/accounts/change_password/', follow=True)
        self.assertIn(b'<h1>Login</h1>', response.content)

    def test_users_orders_when_user_logged_in(self):
        """Test users orders when a user is logged in"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/accounts/orders/', follow=True)
        self.assertIn(
            b'<p class="text-center text-muted">View all your previous orders here.</p>',
            response.content
        )

    def test_users_orders_when_user_logged_out(self):
        """Test where the change passowrd should return to login page if
        no user logged in"""
        response = self.client.get('/accounts/orders/', follow=True)
        self.assertIn(b'<h1>Login</h1>', response.content)

    def test_register_when_not_logged_in(self):
        """Test register page when a user isnt logged in"""
        response = self.client.get('/accounts/register/')
        self.assertIn(b'<h1>Register</h1>', response.content)

    def test_register_when_logged_in(self):
        """Test register page when a user is logged in
        should redirect (302 response)"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/accounts/register/', follow=True)
        self.assertIn(
            b'<h1 class="display-4">Welcome to Project Parts</h1>',
            response.content
        )

    def test_successful_registration(self):
        """Test registration of a user (successful)
        should redirect"""
        response = self.client.post(
            '/accounts/register/',
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'test',
                'email': 'test@example.com',
                'password1': 'examplepassword',
                'password2': 'examplepassword'
            },
            follow=True
        )
        self.assertIn(b'You have successfully registered.', response.content)

    def test_change_password_post(self):
        """Test change password post successful"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.post(
            '/accounts/change_password/',
            {
                'old_password': 'testpassword',
                'new_password1': 'newtestpassword',
                'new_password2': 'newtestpassword'
            },
            follow=True
        )
        self.assertIn(b'Password has been updated', response.content)

    def test_profile_page_post_billing_information(self):
        """Test post on profile page to update billing / shipping information"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.post(
            '/accounts/profile/',
            {
                'address_line_1': '4 High Street',
                'address_line_2': 'Address Line 2',
                'town_city': 'Sandford',
                'county': 'Cheshire',
                'country': 'UK',
                'postcode': 'WA7 2NZ',
            },
            follow=True
        )
        self.assertIn(
            b'<input type="text" name="address_line_1" value="4 High Street" maxlength="40" class=" form-control" required id="id_address_line_1">',
            response.content
        )

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

    def test_register_form_existing_email_data(self):
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

class TestAccountsApp(TestCase):
    """Test Accounts App"""
    def test_accounts_app(self):
        """Test Accounts App"""
        self.assertEqual("accounts", AccountsConfig.name)

class TestAccountsUtils(TestCase):
    """Test Utils function in accounts app"""

    def setUp(self):
        """Set database for tests"""
        self.user = {
            'username': 'test user',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)
        Competition.objects.create(is_active=True, next_competition=False)
        category = Categories(
            category="Exterior"
        )
        category.save()
        manufacturer = Manufacturer(
            name="Eibach"
        )
        manufacturer.save()
        product = Product(
            name="Test Product",
            description="Description",
            img="",
            category=category,
            ticket_price="2.50",
            product_price="795",
            product_link="https://www.github.com",
            part_manufacturer=manufacturer
        )
        product.save()
        user = User.objects.get(
            username='test user'
        )
        OrderItem(
            user=user,
            product=product,
            is_paid=True,
            quantity=5
        ).save()

    def test_get_users_orders_correct_answer(self):
        """Test get users orders where the order answer was correct"""
        user = User.objects.all().first()
        comp = Competition.objects.all().first()
        orderitems = OrderItem.objects.all().first()
        orders = Order.objects.create(
            user=user,
            related_competition=comp,
            answer_correct=True,
            order_date=timezone.now(),
            payment_id='test_payment_id'
        )
        orders.items.add(orderitems)
        Entries.objects.create(
            user=user,
            competition_entry=comp,
            orderItem=orderitems,
            order=orders,
            ticket_number=124
        )

        orders_for_test = Order.objects.filter(
            user=user,
            related_competition=comp,
            answer_correct=True,
            payment_id='test_payment_id'
        )

        response = get_users_orders(orders_for_test)

        self.assertEqual(response[0][0].id, 1)
        self.assertEqual(response[0][1], 12.50)
        self.assertTrue(response[0][2])
        self.assertEqual(response[0][3][0][0][0].name, 'Test Product')
        self.assertEqual(response[0][3][0][0][2][0], 124)

    def test_get_users_orders_incorrect_answer(self):
        """Test get users orders where the order answer was incorrect"""
        user = User.objects.all().first()
        comp = Competition.objects.all().first()
        orderitems = OrderItem.objects.all().first()
        orders = Order.objects.create(
            user=user,
            related_competition=comp,
            answer_correct=False,
            order_date=timezone.now(),
            payment_id='test_payment_id'
        )
        orders.items.add(orderitems)

        orders_for_test = Order.objects.filter(
            user=user,
            related_competition=comp,
            answer_correct=False,
            payment_id='test_payment_id'
        )

        response = get_users_orders(orders_for_test)

        self.assertEqual(response[0][0].id, 2)
        self.assertEqual(response[0][1], 12.50)
        self.assertFalse(response[0][2])
        self.assertEqual(response[0][3][0][0][0].name, 'Test Product')
