"""Unittests for Django polls application."""
import datetime
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question, Choice


def create_question(question_text, pub_date, end_date):
    """
    Create a question with the given `question_text` and published the.

    given number of `days` offset to now (negative for questions published.
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=pub_date)
    time2 = timezone.now() + datetime.timedelta(days=end_date)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time2)


class VotingTests(TestCase):

    def setUp(self):
        User.objects.create_user(username='bhatara007', password='ddddd007')
        self.client.login(username='bhatara007', password='ddddd007')
        self.question = create_question("What is your gender?", pub_date=-4, end_date=5)
        self.choice1 = Choice(id=1, question=self.question, choice_text="male")
        self.choice2 = Choice(id=2, question=self.question, choice_text="female")
        self.choice1.save()
        self.choice2.save()

    def test_authenticated_user_can_replace_thier_vote(self):
        reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id}
        self.first_choice = self.question.choice_set.get(pk=self.choice1.id)
        self.assertEqual(self.choice1.vote_set.all().count(), 1)
        reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice2.id}
        self.second_choice = self.question.choice_set.get(pk=self.choice2.id)
        self.first_choice = self.question.choice_set.get(pk=self.choice1.id)
        self.assertEqual(self.choice2.vote_set.all().count(), 1)
        self.assertEqual(self.choice1.vote_set.all().count(), 0)

    def test_previous_vote_show_correctly(self):
        url = reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id}
        response1 = self.client.get(url)
        self.assertContains(response1, self.choice1.choice_text)
        url = reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id}
        response2 = self.client.get(url)
        self.assertNotContains(response2, self.choice1.choice_text)


if __name__ == '__main__':
    unittest.main()
