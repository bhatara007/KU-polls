"""The view configuration for Django polls app."""
import datetime
import logging

from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote

log = logging.getLogger("polls")
logging.basicConfig(level=logging.INFO)

def get_client_ip(request):
    """Get the client's ip address."""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    """Log when user login success."""
    log.info(f'{user.username} login from ip: {get_client_ip(request)} date: {str(datetime.now())}')


@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    """Log when user logout success."""
    log.info(f'{user.username} logout from ip: {get_client_ip(request)} date: {str(datetime.now())}')


@receiver(user_login_failed)
def log_user_login_failed(sender, request, credentials, **kwargs):
    """Log when user login failed."""
    log.warning(f'{request.POST["username"]} login failed form ip: {get_client_ip(request)} date: {str(datetime.now())}')

@login_required
def detail_view(request, pk):
    """Show the detail of the question or error when vote is not allowed."""
    question = get_object_or_404(Question, pk=pk)
    last_vote = "None"
    selected_vote = False
    if Vote.objects.filter(user = request.user, question = question):
        last_vote = Vote.objects.filter(user = request.user, question = question).first().choice.choice_text
        selected_vote = True
    return render(request, 'polls/detail.html', {'question': question, 'last_vote': last_vote, 'selected_vote': selected_vote})


class IndexView(generic.ListView):
    """The class that contains configuration for Index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be.

        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-end_date')[:]


# class DetailView(generic.DetailView):
#     """The class that contains configuration for Detail page."""

#     model = Question
#     template_name = 'polls/detail.html'

#     def get_queryset(self):
#         """Excludes any questions that aren't published yet."""
#         return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """The class that contains configuration for result page."""

    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """Add vote function to each poll."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        log.info(f'{request.user} submitted a vote for question {question.question_text} form ip: {get_client_ip(request)} date: {datetime.now}  ')
        Vote.objects.update_or_create(user = request.user, question = question, defaults= {'choice': selected_choice})
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
