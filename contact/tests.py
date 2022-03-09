from django.test import TestCase
from django.contrib.auth.models import User
from competition.models import Competition
from .forms import ContactForm
from .apps import ContactConfig

# Create your tests here.

class TestContactPage(TestCase):
    """view tests"""
    def setUp(self):
        self.user = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': 'test user',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)
        Competition(is_active=True).save()

    def test_contact_page_response(self):
        """Test response of contact page"""
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    # def test_contact_post(self):
    #     """Test post for contact page"""
    #     response = self.client.post(
    #         '/contact/',
    #         data={
    #             'email': "test@google.com",
    #             'subject': "Test Subject",
    #             'message': "Here is a test message"
    #         }
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_invalid_form_in_post(self):
    #     """Test invalid for data and return variables"""
    #     response = self.client.post(
    #         '/contact/',
    #         {
    #             'email': "",
    #             'subject': "Test Subject",
    #             'message': "Here is a test message"
    #         }
    #     )
    #     self.assertJSONEqual(
    #         str(response.content, encoding='utf8'),
    #         {
    #             'sent': False,
    #             'error': 'Invalid Form'
    #         }
    #     )

    def test_email_populating_when_logged_in(self):
        """Test that the email field is prepopulating with
        logged in users email"""
        self.client.post(
            '/accounts/login/',
            self.user
        )
        response = self.client.get('/contact/')
        self.assertIn(
            b'<input type="email" name="email" value="test@gmail.com"',
            response.content
        )

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

class TestContactApp(TestCase):
    """Test Contact App"""
    def test_contact_app(self):
        """Test Contact App"""
        self.assertEqual("contact", ContactConfig.name)
