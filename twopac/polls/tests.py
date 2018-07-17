import datetime

from django.test  import TestCase
from django.utils import timezone
from django.urls  import reverse

from .models import Question


def create_question(question_text, days):
  time = timezone.now() + datetime.timedelta(days=days)

  return Question.objects.create(question_text=question_text, publish_date=time)

class QuestionModelTests(TestCase):
  def test_was_published_recently_in_the_future(self):
    """
    was_published_recently() returns False for future publish_date's
    """
    time            = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(publish_date=time)

    self.assertIs(future_question.was_published_recently(), False)

class QuestionIndexViewTests(TestCase):
  def test_no_questions(self):
    """
    If no questions exist ..
    """
    response = self.client.get(reverse('polls:index'))

    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")

    self.assertQuerysetEqual(response.context['latest_top'], [])

  def test_future_question(self):
    """
    Questions in the future don't exist yet.
    """
    create_question(question_text="Future question.", days=30)

    response = self.client.get(reverse('polls:index'))
    self.assertContains(response, "No polls are available.")

    self.assertQuerysetEqual(response.context['latest_top'], [])
  
  def test_two_past_questions(self):
    """
    Index page can display multiple questions
    """
    create_question(question_text="Past 1", days=-30)
    create_question(question_text="Past 2", days=-6)

    response = self.client.get(reverse('polls:index'))

    self.assertQuerysetEqual(
      response.context['latest_top'],
      ['<Question: Past 2>', '<Question: Past 1>']
    )
    