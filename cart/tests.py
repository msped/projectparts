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
        self.assertEqual(
            str(test_name),
            'Order {} - Paid False'.format(test_name.id)
        )

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

    def test_add_to_cart_view(self):
        """Test adding a product to the cart"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        add_product = self.client.post(
            '/cart/add/',
            {
                'qty': '10',
                'product_id': '1'
            }
        )
        self.assertJSONEqual(
            str(add_product.content, encoding='utf8'),
            {'cart_amount': 1}
        )

    def test_increase_item_view_for_ajax_request(self):
        """Test increase an orders quantity by one"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        user = User.objects.all().first()
        comp = Competition.objects.all().first()
        product = Product.objects.all().first()
        order = Orders.objects.create(
            user=user,
            quantity=1,
            related_competition=comp,
            product=product
        )
        order.save()
        add_one_product = self.client.get(
            '/cart/add_one/' + str(order.id)
        )
        self.assertJSONEqual(
            str(add_one_product.content, encoding='utf8'),
            {'qty': 2, 'total': '5.00'}
        )

    def test_decrease_item_view_for_ajax_request(self):
        """Test dencrease an orders quantity by one"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        user = User.objects.all().first()
        comp = Competition.objects.all().first()
        product = Product.objects.all().first()
        order = Orders.objects.create(
            user=user,
            quantity=2,
            related_competition=comp,
            product=product
        )
        order.save()
        add_one_product = self.client.get(
            '/cart/remove_one/' + str(order.id)
        )
        self.assertJSONEqual(
            str(add_one_product.content, encoding='utf8'),
            {'qty': 1, 'total': '2.50'}
        )
