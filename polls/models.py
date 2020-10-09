"""Question and choice class for Django polls."""
import datetime

from django.db import models
from django.utils import timezone


def count_votes():
    """Count votes method."""
    count = 0
    for c in Question.objects.get(pk=id).choices_set.all():
        count = c.votes
    return count


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
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return a string represent for Choice class."""
        return self.choice_text
