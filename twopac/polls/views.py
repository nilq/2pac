from django.shortcuts import render, HttpResponse
from django.template  import loader

from .models import Question


def index(request):
  latest_top = Question.objects.order_by('-publish_date')[:5]
  
  template = loader.get_template('polls/index.html')

  context = {
    'latest_top': latest_top
  }

  return HttpResponse(template.render(context, request))

def detail(question, question_id):
  return HttpResponse("You're looking at question %s" % question_id)

def results(request, question_id):
  response = "You're looking at the results of question %s"
  return HttpResponse(response % question_id)

def vote(request, question_id):
  return HttpResponse("You're voting on question %s" % question_id)
