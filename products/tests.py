from django.test import TestCase
from products.models import Product, Vehicle, Categories, Manufacturer
from .apps import ProductsConfig

# Create your tests here.

class VehicleModelTests(TestCase):
    """Test Vehicle Model"""

    def test_str(self):
        """Test __str__ return"""
        test_name = Vehicle(make='Mercedes', model='A Class', generation="W176")
        self.assertEqual(str(test_name), 'Mercedes A Class W176')

    def test_vehicle_creation(self):
        """Test creation of a vehicle"""
        vehicle = Vehicle(
            make="Ford",
            model="Focus",
            generation="MK3"
        )
        vehicle.save()

        self.assertEqual(vehicle.make, 'Ford')
        self.assertEqual(vehicle.model, 'Focus')
        self.assertEqual(vehicle.generation, 'MK3')

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

    def setUp(self):
        Vehicle.objects.create(
            make="Mercedes",
            model="A Class",
            generation="W176"
        )

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
            model="A Class",
            generation="W176"
        )
        manufacturer = Manufacturer(
            name="Test Manufacturer"
        )
        manufacturer.save()
        prod = Product(
            name="Test Product",
            description="Description",
            category=category,
            ticket_price="2.50",
            product_price="795",
            product_link="https://www.github.com",
            fits=vehicle,
            part_manufacturer=manufacturer
        )
        prod.save()
        response = self.client.get('/tickets/' + str(prod.id) +'/')
        self.assertEqual(response.status_code, 200)

    def test_get_models(self):
        """Test return on get_models view and response"""
        response = self.client.post(
            '/tickets/models/',
            {'make': 'Mercedes'}
        )
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            ['A Class']
        )

    def test_get_gens(self):
        """Test return on get_gens view and response"""
        response = self.client.post(
            '/tickets/gens/',
            {
                'make': 'Mercedes',
                'model': 'A Class'
            }
        )
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            ['W176']
        )

class ProductModelTests(TestCase):
    """Tests for products Model"""

    def test_str(self):
        """Test __str__ return"""
        manufacturer = Manufacturer(
            name="Test"
        )
        manufacturer.save()
        test_name = Product(name='Product', part_manufacturer=manufacturer)
        self.assertEqual(str(test_name), 'Test Product')

    def test_product_creation_no_image(self):
        """Test product model"""
        category = Categories(
            category="Exterior"
        )
        category.save()
        vehicle = Vehicle(
            make="Mercedes",
            model="A Class",
            generation="W176"
        )
        vehicle.save()
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
            fits=vehicle,
            part_manufacturer=manufacturer
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
        self.assertEqual(product.fits.generation, 'W176')
        self.assertEqual(product.part_manufacturer.name, 'Eibach')

    def test_product_fits_multiple_true(self):
        """Test product model"""
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
            part_manufacturer=manufacturer,
            fits_multiple=True
        )
        product.save()

        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'Description')
        self.assertEqual(product.img, '')
        self.assertEqual(product.category.category, 'Exterior')
        self.assertEqual(product.ticket_price, '2.50')
        self.assertEqual(product.product_price, '795')
        self.assertEqual(product.product_link, 'https://www.github.com')
        self.assertEqual(product.part_manufacturer.name, 'Eibach')
        self.assertTrue(product.fits_multiple)

    def test_product_fits_multiple_false(self):
        """Test product model with fits multiple as false"""
        category = Categories(
            category="Exterior"
        )
        category.save()
        vehicle = Vehicle(
            make="Mercedes",
            model="A Class",
            generation="W176"
        )
        vehicle.save()
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
            fits=vehicle,
            part_manufacturer=manufacturer
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
        self.assertEqual(product.fits.generation, 'W176')
        self.assertEqual(product.part_manufacturer.name, 'Eibach')
        self.assertFalse(product.fits_multiple)

class ManufacturerModelTests(TestCase):
    """Test Vehicle Model"""

    def test_str(self):
        """Test __str__ return"""
        test_name = Manufacturer(name='CarbonWurks')
        self.assertEqual(str(test_name), 'CarbonWurks')

    def test_vehicle_creation(self):
        """Test creation of a vehicle"""
        manufacturer = Manufacturer(
            name="CarbonWurks",
        )
        manufacturer.save()

        self.assertEqual(manufacturer.name, 'CarbonWurks')

class TestProductsApp(TestCase):
    """Test Products App"""
    def test_products_app(self):
        """Test Products App"""
        self.assertEqual("products", ProductsConfig.name)
