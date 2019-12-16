from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product, Vehicle, Categories
from competition.models import Competition
from .models import Orders

# Create your tests here.
class CartAppTest(TestCase):
    """Test Order Model"""
    def setUp(self):
        self.user = {
            'username': 'test user',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)
        Competition.objects.create(
            tickets=5000,
            tickets_left=5000,
            question="Is this a test?",
            answer_1="Yes",
            answer_2="No",
            answer_3="Maybe",
            correct_answer="Yes",
            is_active=True
        )
        category = Categories(
            category="Exterior"
        )
        category.save()
        vehicle = Vehicle(
            make="Mercedes",
            model="A Class"
        )
        vehicle.save()
        product = Product(
            name="Test Product",
            description="Description",
            img="",
            category=category,
            ticket_price="2.50",
            product_price="795",
            product_link="https://www.github.com",
            fits=vehicle
        )
        product.save()

    def test_str(self):
        """Test str return"""
        user_test = User.objects.get(username='test user')
        comp_test = Competition.objects.get(is_active=True)
        product_test = Product.objects.filter().first()
        test_name = Orders.objects.create(
            user=user_test,
            related_competition=comp_test,
            quantity=1,
            product=product_test
        )
        self.assertEqual(str(test_name), 'Order 3 - Paid False')

    def test_cart_page_response_user_logged_in(self):
        """Test cart response for when a user is logged in,
        should return the cart page"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/cart/', follow=True)
        self.assertIn(b'<h1 class="text-center">Cart</h1>', response.content)

    def test_cart_page_response_user_not_logged_in(self):
        """Test cart response for when a user isn't logged in,
        should return the login page"""
        response = self.client.get('/cart/', follow=True)
        self.assertIn(b'<h1>Login</h1>', response.content)

    def test_remove_test(self):
        """Test remove item view, should delete item from DB"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/cart/remove/1', follow=True)
        self.assertIn(b'Ticket(s) Removed.', response.content)
