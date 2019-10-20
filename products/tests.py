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
