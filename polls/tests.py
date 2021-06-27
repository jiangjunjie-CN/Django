import datetime
from django.utils import timezone
from .models import Question
from django.test import TestCase

# Create your tests here.
class QuestionMethodTests(TestCase):
    def test_was_published_recently_no_include_future(self):
        '''
        发布于未来的问题使用was_published_recently应该返回false
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_q = Question(pub_date=time)
        self.assertIs(future_q.was_publish_recently(), False)