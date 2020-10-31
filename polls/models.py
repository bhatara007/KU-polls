"""Question and choice class for Django polls."""
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Question(models.Model):
    """Question class for Django poll Application."""

    search_fields = ['question_text']
    list_filter = ['pub_date', 'end_date']
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    '''create datetime field for end_date'''
    end_date = models.DateTimeField('Date the polls expires')

    def __str__(self):
        """Represent String method for models class."""
        return self.question_text

    def was_published_recently(self):
        """Check Question that published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check Question that published or not."""
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Check Question that can vote or not."""
        now = timezone.now()
        return self.pub_date <= now <= self.end_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.admin_order_field = 'end_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Choice class for Django poll Application."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    
    @property
    def votes(self):
        """Return the number of vote for each question."""
        return self.question.vote_set.filter(choice=self).count()

    def __str__(self):
        """Return a string represent for Choice class."""
        return self.choice_text
    

class Vote(models.Model):
    """Vote class for Django poll Application."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
