from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product, Vehicle, Categories, Manufacturer
from competition.models import Competition
from .models import Order, OrderItem
from .apps import CartConfig

# Create your tests here.
class CartAppTest(TestCase):
    """Test Order Model"""
    def setUp(self):
        self.user = {
            'username': 'test user',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        self.user2 = {
            'username': 'test user 2',
            'email': 'test2@gmail.com',
            'password': 'testpassword2'
        }
        User.objects.create_user(**self.user)
        User.objects.create_user(**self.user2)
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
        manufacturer = Manufacturer(
            name="Test Manufacturer"
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

        user = User.objects.get(email='test@gmail.com')
        comp = Competition.objects.get(is_active=True)
        order = Order(
            user=user,
            related_competition=comp,
            order_date=timezone.now()
        )
        order.save()

    def test_order_item_str(self):
        """Test str return"""
        user_test = User.objects.get(username='test user')
        product_test = Product.objects.filter().first()
        test_name = OrderItem.objects.create(
            user=user_test,
            quantity=1,
            product=product_test
        )
        self.assertEqual(
            str(test_name),
            '1 of Test Product'
        )

    def test_order_str(self):
        """Test str return of the order model"""
        user = User.objects.get(username='test user')
        comp = Competition.objects.get(is_active=True)
        product = Product.objects.filter().first()
        item = OrderItem.objects.create(
            user=user,
            quantity=1,
            product=product
        )
        order = Order.objects.create(
            user=user,
            related_competition=comp,
            order_date=timezone.now(),
            payment_id='test_id_stripe'
        )
        order.items.add(item)

        self.assertEqual(order.user.username, 'test user')
        self.assertEqual(order.related_competition.id, comp.id)
        self.assertEqual(order.payment_id, 'test_id_stripe')

    def test_cart_page_response(self):
        """Test cart page response"""
        response = self.client.get('/cart/', follow=True)
        self.assertIn(b'<h1 class="text-center">Cart</h1>', response.content)

    # Test cart when a user is logged in (database)
    def test_add_to_cart_view_logged_in_not_in_cart(self):
        """Test adding a product to the cart using the database with
        item not in the cart"""
        product = Product.objects.all().first()
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        add_product = self.client.post(
            '/cart/add/',
            {
                'qty': '10',
                'product_id': str(product.id)
            }
        )
        self.assertJSONEqual(
            str(add_product.content, encoding='utf8'),
            {'cart_amount': 1}
        )

    def test_add_to_cart_view_logged_in_in_cart(self):
        """Test adding a product to the cart using the database with
        item not the cart"""
        product = Product.objects.all().first()
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        self.client.post(
            '/cart/add/',
            {
                'qty': '10',
                'product_id': str(product.id)
            }
        )
        add_product = self.client.post(
            '/cart/add/',
            {
                'qty': '10',
                'product_id': str(product.id)
            }
        )
        self.assertJSONEqual(
            str(add_product.content, encoding='utf8'),
            {'cart_amount': 1}
        )

    def test_increase_item_view_for_ajax_request_logged_in(self):
        """Test increase an orders quantity by one"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        user = User.objects.all().first()
        product = Product.objects.all().first()
        comp = Competition.objects.all().first()
        order = Order.objects.get(
            user=user,
            related_competition=comp
        )
        orderitem = OrderItem.objects.create(
            user=user,
            quantity=2,
            product=product
        )
        orderitem.save()
        orderitem = OrderItem.objects.get(
            user=user,
            quantity=2,
            product=product
        )
        order.items.add(orderitem)
        add_one_product = self.client.get(
            '/cart/add_one/' + str(orderitem.id)
        )
        self.assertJSONEqual(
            str(add_one_product.content, encoding='utf8'),
            {'qty': 3, 'total': '7.50'}
        )

    def test_decrease_item_view_for_ajax_request_logged_in(self):
        """Test decrease an orders quantity by one"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        user = User.objects.all().first()
        product = Product.objects.all().first()
        comp = Competition.objects.all().first()
        order = Order.objects.get(
            user=user,
            related_competition=comp
        )
        orderitem = OrderItem.objects.create(
            user=user,
            quantity=2,
            product=product
        )
        orderitem.save()
        orderitem = OrderItem.objects.get(
            user=user,
            quantity=2,
            product=product
        )
        order.items.add(orderitem)
        remove_one_product = self.client.get(
            '/cart/remove_one/' + str(orderitem.id)
        )
        # total has to be 
        self.assertJSONEqual(
            str(remove_one_product.content, encoding='utf8'),
            {'qty': 1, 'total': '2.50'}
        )

    def test_remove_cart_item_ajax_request_logged_in(self):
        """Test remove item, should delete item from DB"""
        self.client.post(
            '/accounts/login/',
            self.user,
            follow=True
        )
        user = User.objects.all().first()
        product = Product.objects.all().first()
        order = OrderItem.objects.create(
            user=user,
            quantity=2,
            product=product
        )
        order.save()
        remove_product = self.client.post(
            '/cart/remove/',
            {
                'order_id': int(order.id)
            }
        )
        self.assertJSONEqual(
            str(remove_product.content, encoding='utf8'),
            {'total': 0, 'cart_amount': 0}
        )

    # Test cart when a user isn't logged in (session)
    def test_add_to_cart_view_logged_out_not_in_cart(self):
        """Test adding a product to the cart using the session"""
        product = Product.objects.all().first()
        add_product = self.client.post(
            '/cart/add/',
            {
                'qty': '2',
                'product_id': str(product.id)
            }
        )
        session = self.client.session
        self.assertIn(str(product.id), session['cart'])
        self.assertJSONEqual(
            str(add_product.content, encoding='utf8'),
            {'cart_amount': 1}
        )

    def test_add_to_cart_view_logged_out_in_cart(self):
        """Test adding a product to the cart using the session with
        the product in the cart"""
        product = Product.objects.all().first()
        self.client.post(
            '/cart/add/',
            {
                'qty': '2',
                'product_id': str(product.id)
            }
        )
        add_product = self.client.post(
            '/cart/add/',
            {
                'qty': '2',
                'product_id': str(product.id)
            }
        )
        session = self.client.session
        self.assertIn(str(product.id), session['cart'])
        self.assertJSONEqual(
            str(add_product.content, encoding='utf8'),
            {'cart_amount': 1}
        )

    def test_increase_item_view_for_ajax_request_logged_out(self):
        """Test increase an orders quantity by one"""
        order = Order.objects.all().first()
        self.client.post(
            '/cart/add/',
            {
                'qty': '2',
                'product_id': str(order.id)
            }
        )
        add_one_product = self.client.get(
            '/cart/add_one/' + str(order.id)
        )
        session = self.client.session
        self.assertIn(str(order.id), session['cart'])
        self.assertJSONEqual(
            str(add_one_product.content, encoding='utf8'),
            {'qty': 3, 'total': '7.50'}
        )

    def test_decrease_item_view_for_ajax_request_logged_out(self):
        """Test decrease an orders quantity by one"""
        order = Order.objects.all().first()
        self.client.post(
            '/cart/add/',
            {
                'qty': '2',
                'product_id': str(order.id)
            }
        )
        remove_one = self.client.get(
            '/cart/remove_one/' +str(order.id)
        )
        session = self.client.session
        self.assertIn(str(order.id), session['cart'])
        self.assertJSONEqual(
            str(remove_one.content, encoding='utf8'),
            {'qty': 1, 'total': '2.50'}
        )

    def test_remove_cart_item_ajax_request_logged_out(self):
        """Test remove item view, should pop item from session"""
        self.client.post(
            '/cart/add/',
            {
                'qty': '10',
                'product_id': '4'
            }
        )
        remove_order = self.client.post(
            '/cart/remove/',
            {
                'order_id': '4'
            }
        )
        session = self.client.session
        self.assertNotIn('4', session['cart'])
        self.assertJSONEqual(
            str(remove_order.content, encoding='utf8'),
            {'total': 0, 'cart_amount': 0}
        )

    def test_cart_response_no_items(self):
        """Test cart page response """
        response = self.client.get('/cart/')
        self.assertIn(
            b'<p class="text-center no-cart-items">There are no items in your cart, add some <a href="/tickets/">tickets.</a></p>',
            response.content
        )

    def test_cart_app(self):
        """Test Cart App"""
        self.assertEqual("cart", CartConfig.name)
