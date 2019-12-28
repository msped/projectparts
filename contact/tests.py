from django.test import TestCase
from .forms import ContactForm

# Create your tests here.

class TestContactPage(TestCase):
    """view tests"""
    def test_contact_page_response(self):
        """Test response of contact page"""
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_contact_post(self):
        """Test post for contact page"""
        response = self.client.post(
            '/contact/',
            data={
                'email': "test@google.com",
                'subject': "Test Subject",
                'message': "Here is a test message"
            }
        )
        self.assertEqual(response.status_code, 200)

class TestContactForm(TestCase):
    """Contact form tests"""
    def test_contact_form_valid_response(self):
        """Test full working contact form"""
        form = ContactForm({
            'email': 'test@email.com',
            'subject': 'test subject',
            'message': 'test message'
        })
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_email(self):
        """Test full working contact form"""
        form = ContactForm({
            'email': 'testemail.com',
            'subject': 'test subject',
            'message': 'test message'
        })
        self.assertFalse(form.is_valid())

    def test_contact_form_invalid_subject(self):
        """Test full working contact form"""
        form = ContactForm({
            'email': 'test@email.com',
            'subject': '',
            'message': 'test message'
        })
        self.assertFalse(form.is_valid())

    def test_contact_form_invalid_message(self):
        """Test full working contact form"""
        form = ContactForm({
            'email': 'test@email.com',
            'subject': 'test subject',
            'message': ''
        })
        self.assertFalse(form.is_valid())

    def test_contact_form_empty(self):
        """Test full working contact form"""
        form = ContactForm({
            'email': '',
            'subject': '',
            'message': ''
        })
        self.assertFalse(form.is_valid())
