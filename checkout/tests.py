from django.test import TestCase
from django.contrib.auth.models import User
from competition.models import Competition
from cart.models import Orders
from products.models import Product, Vehicle, Categories, Manufacturer
from .models import Entries
from .utils import get_total, get_users_tickets
from .forms import PaymentForm

# Create your tests here.
class TestCheckoutApp(TestCase):
    """All tests for the Checkout App"""

    def setUp(self):
        self.user = {
            'username': 'test user',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)
        user = User.objects.all().first()
        Competition(
            is_active=True,
            question="Is this a test?",
            answer_1="Yes",
            answer_2="No",
            answer_3="Maybe",
            correct_answer="Yes"
        ).save()
        comp = Competition.objects.all().first()
        category = Categories.objects.create(
            category="Exterior"
        )
        vehicle = Vehicle.objects.create(
            make="Mercedes",
            model="A Class",
            generation="W176"
        )
        man = Manufacturer.objects.create(
            name="Test Manu"
        )
        Product.objects.create(
            name="Test Product",
            description="Description",
            img="media/default.jpg",
            category=category,
            ticket_price="2.50",
            product_price="795",
            product_link="https://www.github.com",
            fits=vehicle,
            part_manufacturer=man
        )
        product = Product.objects.all().first()
        Orders(
            user=user,
            product=product,
            is_paid=False,
            related_competition=comp,
            quantity=5
        ).save()

    def test_checkout_view_logged_in(self):
        """Test the get request for checkout view"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/checkout/', follow=True)
        self.assertIn(b'<h1>Checkout</h1>', response.content)

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
        order = Orders.objects.all().first()
        entry_str = Entries.objects.create(
            user=user,
            competition_entry=comp,
            order=order,
            ticket_number=100
        )
        self.assertEqual(
            str(entry_str),
            'Competition {}: Ended | Ticket No: 100'.format(comp.id)
        )

    def test_entries_model(self):
        """Test the entries model"""
        user = User.objects.all().first()
        comp = Competition.objects.all().first()
        order = Orders.objects.all().first()
        entry = Entries.objects.create(
            user=user,
            competition_entry=comp,
            order=order,
            ticket_number=124
        )
        self.assertEqual(entry.user.email, 'test@gmail.com')
        self.assertEqual(entry.ticket_number, 124)

    def test_payment_form(self):
        """Test payment form"""
        form = PaymentForm({
            'credit_card_number': '4242424242424242',
            'cvv': '444',
            'expiry_month': '12',
            'expiry_year': '2020',
            'stripe_id': 'testID'
        })
        self.assertTrue(form.is_valid())

    def test_get_total_util(self):
        """Test utils function get_total"""
        orders = Orders.objects.all()
        total = get_total(orders)
        self.assertEqual(float(total), 12.50)

    def test_get_users_tickets(self):
        """Test utils function to get users ticket amount"""
        orders = Orders.objects.all()
        ticket_amount = get_users_tickets(orders)
        self.assertEqual(ticket_amount, 5)
