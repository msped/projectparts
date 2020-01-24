from django.test import TestCase
from .models import Competition
from .apps import CompetitionConfig

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
