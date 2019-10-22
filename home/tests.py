from django.test import TestCase

# Create your tests here.

class HomeViewTests(TestCase):
    """Home App Test"""
    def test_home_page_status_code(self):
        """Test Home Page Response"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        