from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from .models import Competition
from .apps import CompetitionConfig
from .utlis import (
    new_competition,
    check_for_new_competition
)   

# Create your tests here.

class ModelTest(TestCase):
    """Test for Competition Model"""

    def test_str_comp_pending(self):
        """Test str return for competition that is pending"""
        comp = Competition(
            tickets=5000,
            tickets_left=5000,
            question="Is this a test?",
            answer_1="Yes",
            answer_2="No",
            answer_3="Maybe",
            correct_answer="Yes"
        )
        comp.save()

        self.assertEqual(str(comp), f"Competition {comp.id}: Pending")

    def test_str_comp_active(self):
        """Test str return for competition that is active"""
        comp = Competition(
            tickets=5000,
            tickets_left=5000,
            question="Is this a test?",
            answer_1="Yes",
            answer_2="No",
            answer_3="Maybe",
            correct_answer="Yes",
            is_active=True
        )
        comp.save()

        self.assertEqual(str(comp), f"Competition {comp.id}: 5000")

    def test_str_comp_ended(self):
        """Test str return for competition has ended"""
        comp = Competition(
            tickets=5000,
            tickets_left=0,
            question="Is this a test?",
            answer_1="Yes",
            answer_2="No",
            answer_3="Maybe",
            correct_answer="Yes"
        )
        comp.save()

        self.assertEqual(str(comp), f"Competition {comp.id}: Ended")

    def test_create_competition(self):
        """Test creation of a competition"""
        comp = Competition(
            tickets=5000,
            tickets_left=5000,
            question="Is this a test?",
            answer_1="Yes",
            answer_2="No",
            answer_3="Maybe",
            correct_answer="Yes"
        )
        comp.save()

        self.assertEqual(comp.tickets, 5000)
        self.assertEqual(comp.tickets_left, 5000)
        self.assertEqual(comp.question, "Is this a test?")
        self.assertEqual(comp.answer_1, "Yes")
        self.assertEqual(comp.answer_2, "No")
        self.assertEqual(comp.answer_3, "Maybe")
        self.assertEqual(comp.correct_answer, "Yes")
        self.assertEqual(comp.is_active, False)

class TestCompetitionViews(TestCase):
    """Test all views in the competition app"""
    def test_winners_page_response(self):
        """Test response of winners page"""
        response = self.client.get('/competition/winners/')
        self.assertEqual(response.status_code, 200)

    def test_get_current_ticket_amount(self):
        """Test reponse of view that returns the current ticket
        amount of the homepage"""
        comp = Competition.objects.create(is_active=True)
        comp.save()
        ticket_amount = self.client.get('/competition/get_current/')
        self.assertEqual(ticket_amount.content, b'4000')

    def test_get_current_ticket_amount_no_comp_active(self):
        """Test reponse of view that returns the current ticket
        amount of the homepage if theres no competition active"""
        comp = Competition.objects.create(is_active=False)
        comp.save()
        ticket_amount = self.client.get('/competition/get_current/')
        self.assertEqual(ticket_amount.content, b'No Competition Active')


class TestCompetitionApp(TestCase):
    """Test Competition App"""
    def test_competition_app(self):
        """Test Competition App"""
        self.assertEqual("competition", CompetitionConfig.name)

class TestUtils(TestCase):
    """Test Util functions"""

    def setUp(self):
        """Set up models for testing"""
        self.user = {
            'first_name': 'Test 1',
            'last_name': 'User 1',
            'username': 'test user',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        self.user2 = {
            'first_name': 'Test 2',
            'last_name': 'User 2',
            'username': 'test user 2',
            'email': 'test2@gmail.com',
            'password': 'testpassword2'
        }
        User.objects.create_user(**self.user)
        User.objects.create_user(**self.user2)
        Competition.objects.create(
            tickets_left=499,
            next_competition=False
        )

    def test_new_competition_result(self):
        """Test that a new competition has been made"""
        new_competition()

        response = Competition.objects.filter(next_competition=True).exists()

        # Check if model has been created
        self.assertTrue(response)

        # Check that mail has been sent to admins
        self.assertEqual(len(mail.outbox), 1)

        # Check that the subject is correct
        self.assertEqual(
            mail.outbox[0].subject,
            'New Competition has been created.'
        )

    def test_check_for_new_competition_found(self):
        """Test function that checks whether a new comeptition should be
        created"""
        comp = Competition.objects.create(
            next_competition=True
        )
        check_for_new_competition(comp)

        response = Competition.objects.filter(next_competition=True).exists()

        self.assertTrue(response)

    def test_check_for_new_competition_creates_new_comp(self):
        """Test function that checks whether a new comeptition should be
        created"""
        comp = Competition.objects.get(tickets_left=499)
        check_for_new_competition(comp)

        response = Competition.objects.filter(next_competition=True).exists()

        self.assertTrue(response)
