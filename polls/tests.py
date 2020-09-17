import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
        
    def test_future_question_can_vote(self):
        '''
        can_vote() method will return False if voted in future question
        '''
        pub = timezone.now() + datetime.timedelta(days=5)
        end = timezone.now() + datetime.timedelta(days=7)
        future_question = Question(pub_date=pub, end_date=end)
        self.assertIs(future_question.can_vote(), False)
    
    def test_past_question_can_vote(self):
        '''
        can_vote() method will return False if voted in past question
        '''
        pub = timezone.now() - datetime.timedelta(days=7)
        end = timezone.now() - datetime.timedelta(days=5)
        past_question = Question(pub_date=pub, end_date=end)
        self.assertIs(past_question.can_vote(), False)
    
    def test_published_question_can_vote(self):
        '''
        can_vote() method will return True if voted in question that not expired
        '''
        pub = timezone.now() + datetime.timedelta(days=-1)
        end = timezone.now() + datetime.timedelta(days=5)
        published_question = Question(pub_date=pub, end_date=end)
        self.assertIs(published_question.can_vote(), True)
    
    def test_published_question(self):
        '''
        is_published() method will return True if poll already published
        '''
        pub = timezone.now() + datetime.timedelta(days=-1)
        end = timezone.now() + datetime.timedelta(days=5)
        published_question = Question(pub_date=pub, end_date=end)
        self.assertIs(published_question.is_published(), True)
    
    def tsst_not_published_question(self):
        '''
        is_published() method will return False if poll not published
        '''
        pub = timezone.now() + datetime.timedelta(days=1)
        end = timezone.now() + datetime.timedelta(days=5)
        not_published_question = Question(pub_date=pub, end_date=end)
        self.assertIs(not_published_question.is_published(), False)
        
def create_question(question_text, pub_date, end_date):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=pub_date)
    time2 = timezone.now() + datetime.timedelta(days=end_date)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time2)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", pub_date=-30, end_date=-29)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", pub_date=30, end_date=31)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", pub_date=-30, end_date=-29 )
        create_question(question_text="Future question.", pub_date=30, end_date=31)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", pub_date=-30, end_date=-29)
        create_question(question_text="Past question 2.", pub_date=-5, end_date=-4)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', pub_date=5, end_date=6)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', pub_date=-5, end_date=-4)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
