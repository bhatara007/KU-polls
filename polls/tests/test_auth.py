"""Unittests for Django polls application."""
import datetime
import unittest

from django.contrib.auth.models import User
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

class UserAuthenticationTest(TestCase):
    
    def setUp(self):
        User.objects.create_user(username = 'bhatara007', password = 'ddddd007')
        self.new_question = create_question(question_text='What are your favorite color?', pub_date=-5, end_date=99)
    
    def test_user_login_success(self):
        '''test user can login and show username on index page.'''
        self.client.login(username='bhatara007', password='ddddd007')
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertContains(response, "bhatara007")
    
    def test_unauthenticated_user_name_not_show_no_index_page(self):
        '''test if user not login thier username doesn't show on index page'''
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertNotContains(response, "bhatara007")
        url = reverse('polls:detail', args=(self.new_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_authenticated_can_access_detail_page(self):
        '''test athenticated user can access to detail page. '''
        self.client.login(username = 'bhatara007', password = 'ddddd007')
        url = reverse('polls:detail', args=(self.new_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_can_not_access_detail_page(self):
        '''test unathenticated user cannot access to detail page. '''
        url = reverse('polls:detail', args=(self.new_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
if __name__ == '__main__':
    unittest.main()