"""The view configuration for Django polls app."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote



@login_required
def detail_view(request, pk):
    """Show the detail of the question or error when vote is not allowed."""
    question = get_object_or_404(Question, pk=pk)
    selected_vote = "None"
    if Vote.objects.filter(user = request.user, question = question):
        selected_vote = Vote.objects.filter(user = request.user, question = question).first().choice.choice_text
    return render(request, 'polls/detail.html', {'question': question, 'selected_vote': selected_vote})



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
        Vote.objects.update_or_create(user = request.user, question = question, defaults= {'choice': selected_choice})
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
