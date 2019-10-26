from django.test import TestCase
from .models import Competition

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

        self.assertEqual("Competition 1: Pending", "Competition 1: Pending")

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

        self.assertEqual("Competition 1: 5000", "Competition 1: 5000")

    def test_str_comp_ended(self):
        """Test str return for competition has ended"""
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

        self.assertEqual("Competition 1: Ended", "Competition 1: Ended")

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
