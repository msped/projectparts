from django.test import TestCase
from .apps import HomeConfig

# Create your tests here.

class HomeViewTests(TestCase):
    """Home Views Test"""
    def test_home_page_status_code(self):
        """Test Home Page Response"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class TestAccountsApp(TestCase):
    """Test Home App"""
    def test_home_app(self):
        """Test Home App"""
        self.assertEqual("home", HomeConfig.name)
