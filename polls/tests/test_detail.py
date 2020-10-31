"""Unittests for Django polls application."""
import datetime
import unittest

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question

def create_question(question_text, pub_date, end_date):
    """
    Create a question with the given `question_text` and published the.

    given number of `days` offset to now (negative for questions published.
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=pub_date)
    time2 = timezone.now() + datetime.timedelta(days=end_date)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time2)

class QuestionDetailViewTests(TestCase):
    """The class that contains a unittest for detail view in django polls app."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future."""
        future_question = create_question(question_text='Future question.', pub_date=5, end_date=6)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past.

        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', pub_date=-5, end_date=-4)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_recent_question(self):
        """If we can access this url status code will return 200."""
        past_question = create_question(question_text='Past Question.', pub_date=-5, end_date=4)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()