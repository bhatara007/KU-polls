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
        self.first_choice = Choice(id=1, question=self.question, choice_text="male")
        self.second_choice = Choice(id=2, question=self.question, choice_text="female")
        self.first_choice.save()
        self.second_choice.save()

    def test_authenticated_user_can_replace_their_vote(self):
        '''test authenticated user can replace their vote in this polls period'''
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice':self.first_choice.id})
        self.first_choice = self.question.choice_set.get(pk = self.first_choice.id)
        self.assertEqual(self.first_choice.vote_set.all().count(), 1)
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice':self.second_choice.id})
        self.second_choice = self.question.choice_set.get(pk = self.second_choice.id)
        self.first_choice = self.question.choice_set.get(pk = self.first_choice.id)
        self.assertEqual(self.second_choice.vote_set.all().count(), 1)
        self.assertEqual(self.first_choice.vote_set.all().count(), 0)
        
    def test_previous_vote_show(self):
        '''test previos vote show on detail page'''
        response1 = self.client.get(reverse('polls:detail', args=(self.question.id,)))
        self.assertContains(response1, "None")
        self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.first_choice.id})
        response1 = self.client.get(reverse('polls:detail', args=(self.question.id,)))
        self.assertNotContains(response1, "None")


if __name__ == '__main__':
    unittest.main()
