from django.test import TestCase
from products.models import Product, Vehicle, Categories

# Create your tests here.

class VehicleModelTests(TestCase):
    """Test Vehicle Model"""

    def test_str(self):
        """Test __str__ return"""
        test_name = Vehicle(make='Mercedes', model='A Class')
        self.assertEqual(str(test_name), 'Mercedes A Class')

    def test_vehicle_creation(self):
        """Test creation of a vehicle"""
        vehicle = Vehicle(
            make="Ford",
            model="Focus"
        )
        vehicle.save()

        self.assertEqual(vehicle.make, 'Ford')
        self.assertEqual(vehicle.model, 'Focus')

class CategoriesModelTests(TestCase):
    """Test Categories Model"""

    def test_str(self):
        """Test __str__ return"""
        test_name = Categories(category="Exhaust")
        self.assertEqual(str(test_name), 'Exhaust')

    def test_categories_model_creation(self):
        """Test creation of a category"""
        categories = Categories(
            category='Interior'
        )
        categories.save()

        self.assertEqual(categories.category, 'Interior')

class ProductAppViewsTest(TestCase):
    """Test case for views in the Products"""

    def test_products_page_response_200(self):
        """Test response of the main products page"""
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, 200)

    def test_specific_product_page(self):
        """Test response of a product extra detail page"""
        category = Categories.objects.create(
            category="Exterior"
        )
        vehicle = Vehicle.objects.create(
            make="Mercedes",
            model="A Class"
        )
        Product.objects.create(
            name="Test Product",
            description="Description",
            img="media/default.jpg",
            category=category,
            ticket_price="2.50",
            product_price="795",
            product_link="https://www.github.com",
            fits=vehicle
        )
        response = self.client.get('/tickets/1/')
        self.assertEqual(response.status_code, 200)

class ProductModelTests(TestCase):
    """Tests for products Model"""

    def test_str(self):
        """Test __str__ return"""
        test_name = Product(name='Product')
        self.assertEqual(str(test_name), 'Product')

    def test_product_creation_no_image(self):
        """Test product model"""
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

        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'Description')
        self.assertEqual(product.img, '')
        self.assertEqual(product.category.category, 'Exterior')
        self.assertEqual(product.ticket_price, '2.50')
        self.assertEqual(product.product_price, '795')
        self.assertEqual(product.product_link, 'https://www.github.com')
        self.assertEqual(product.fits.make, 'Mercedes')
        self.assertEqual(product.fits.model, 'A Class')
