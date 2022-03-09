from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from competition.models import Competition
from cart.models import Order, OrderItem
from products.models import Product, Categories, Manufacturer
from .models import Entries
from .utils import update_orders
from .apps import CheckoutConfig

# Create your tests here.
class TestCheckoutApp(TestCase):
    """All tests for the Checkout App"""

    def setUp(self):
        self.user = {
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
        user = User.objects.all().first()
        Competition(
            is_active=True,
            question="Is this a test?",
            answer_1="Yes",
            answer_2="No",
            answer_3="Maybe",
            correct_answer="Yes"
        ).save()
        category = Categories.objects.create(
            category="Exterior"
        )
        man = Manufacturer.objects.create(
            name="Test Manu"
        )
        Product.objects.create(
            slug="test-slug",
            name="Test Product",
            description="Description",
            img="media/default.jpg",
            category=category,
            ticket_price="2.50",
            product_price="795",
            product_link="https://www.github.com",
            part_manufacturer=man
        )
        product = Product.objects.all().first()
        OrderItem(
            user=user,
            product=product,
            is_paid=False,
            quantity=5
        ).save()

    def test_checkout_view_not_logged_in(self):
        """Test the get request for checkout view without user logged in"""
        response = self.client.get('/checkout/', follow=True)
        self.assertIn(b'<h1>Login</h1>', response.content)

    def test_checkout_success_view_not_logged_in(self):
        """Test the get request for checkout view without user logged in"""
        response = self.client.get('/checkout/complete', follow=True)
        self.assertIn(b'<h1>Login</h1>', response.content)

    def test_entries_str(self):
        """Test __str__ return"""
        user = User.objects.all().first()
        comp = Competition.objects.create(is_active=False, tickets_left=0)
        orderitems = OrderItem.objects.all().first()
        order = Order.objects.create(
            user=user,
            related_competition=comp,
            answer_correct=True,
            order_date=timezone.now(),
            payment_id='test_payment_id'
        )
        order.items.add(orderitems)
        entry_str = Entries.objects.create(
            user=user,
            competition_entry=comp,
            orderItem=orderitems,
            order=order,
            ticket_number=124
        )
        self.assertEqual(
            str(entry_str),
            'Competition {}: Ended | Ticket No: 124'.format(comp.id)
        )

    def test_entries_model(self):
        """Test the entries model"""
        user = User.objects.all().first()
        comp = Competition.objects.all().first()
        orderitems = OrderItem.objects.all().first()
        order = Order.objects.create(
            user=user,
            related_competition=comp,
            answer_correct=True,
            order_date=timezone.now(),
            payment_id='test_payment_id'
        )
        order.items.add(orderitems)
        entry = Entries.objects.create(
            user=user,
            competition_entry=comp,
            orderItem=orderitems,
            order=order,
            ticket_number=124
        )
        self.assertEqual(entry.user.email, 'test@gmail.com')
        self.assertEqual(entry.ticket_number, 124)

    def test_checkout_view_no_tickets(self):
        """Test redirect if user has no tickets"""
        self.client.post(
            '/accounts/login/',
            self.user2,
            follow=True
        )
        response = self.client.get('/checkout/', follow=True)
        self.assertIn(b'You have no tickets to checkout.', response.content)

    def test_checkout_view_no_user_answer(self):
        """Test checkout view when no user answer is given"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        user = User.objects.get(username='test user')
        comp = Competition.objects.get(is_active=True)
        orderitems = OrderItem.objects.all().first()
        order = Order.objects.create(
            user=user,
            related_competition=comp,
            answer_correct=True,
            order_date=timezone.now(),
            payment_id='test_payment_id'
        )
        order.items.add(orderitems)
        response = self.client.post(
            '/checkout/',
            {
                'credit_card_number': '4242424242424242',
                'cvv': '477',
                'expiry_month': '5',
                'expiry_year': '2022'
            },
            follow=True
        )
        self.assertIn(
            b'Please select an answer to the question at the bottom of the page',
            response.content
        )

    def test_checkout_app(self):
        """Test Checkout App"""
        self.assertEqual("checkout", CheckoutConfig.name)

    def test_checkout_view_too_many_tickets(self):
        """Test error message if a user has too many tickets compared too
        what is left in the competition"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        user = User.objects.get(username='test user')
        product = Product.objects.all().first()
        comp = Competition.objects.all().first()
        order = Order.objects.create(
            user=user,
            related_competition=comp,
            answer_correct=True,
            order_date=timezone.now(),
            payment_id='test_payment_id'
        )
        o_i = OrderItem.objects.create(
            user=user,
            product=product,
            is_paid=False,
            quantity=4001
        )
        o_i.save()
        orderitem = OrderItem.objects.get(
            user=user,
            product=product,
            is_paid=False,
            quantity=4001
        )
        order.items.add(orderitem)
        order.save()
        response = self.client.post(
            '/checkout/',
            {
                'credit_card_number': '4242424242424242',
                'cvv': '444',
                'expiry_month': '5',
                'expiry_year': '2022',
                'user-answer': 'Yes'
            },
            follow=True
        )
        self.assertIn(
            b'The amount of tickets you have ordered, 4001, is greater\n                        than what is left in the competition, 4000.',
            response.content
        )

class TestUtils(TestCase):
    """Test Util functions"""
    def setUp(self):
        """Set up models for tests"""
        self.user = {
            'username': 'test user',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)
        category = Categories.objects.create(
            category="Exterior"
        )
        man = Manufacturer.objects.create(
            name="Test Manu"
        )
        Product.objects.create(
            slug="test-slug",
            name="Test Product",
            description="Description",
            img="media/default.jpg",
            category=category,
            ticket_price="2.50",
            product_price="795",
            product_link="https://www.github.com",
            part_manufacturer=man
        )
        Competition.objects.create()

    def test_update_orders(self):
        """Test that an order get updated with whether the user answer is
        correct"""
        user = User.objects.filter().first()
        comp = Competition.objects.filter().first()
        product = Product.objects.filter().first()
        OrderItem.objects.create(
            user=user,
            product=product,
            is_paid=False,
            quantity=5
        )
        orderItem = OrderItem.objects.get(
            user=user,
            product=product,
            is_paid=False,
            quantity=5
        )
        tz_now=timezone.now()
        new_order = Order.objects.create(
            user=user,
            related_competition=comp,
            answer_correct=True,
            order_date=tz_now,
        )
        new_order.items.add(orderItem)
        new_order.save()
        order = Order.objects.get(
            user=user,
            related_competition=comp,
            answer_correct=True,
            order_date=tz_now,
        )
        
        update_return = update_orders(comp, order, True, 'test_payment')

        self.assertEqual(update_return.payment_id, 'test_payment')
