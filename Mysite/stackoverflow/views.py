
from stackoverflow.models import Question, Choice
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name=""###
    context_object_name='latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:3]




class DetailView(generic.DetailView):
    model = Question
    template_name=""
    
class ResultsView(DetailView):
    model = Question
    template_name=""
    
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
# Create your views here.
