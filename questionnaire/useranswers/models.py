from django.db import models
from questionnaire.users.models import User
from questionnaire.questions.models import Questions
from questionnaire.answers.models import Answers
from questionnaire.counts.models import Counts


class UserAnswers(models.Model):
    user_id = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Questions, blank=True, on_delete=models.CASCADE)
    answer_id = models.ManyToManyField(Answers, blank=True)
    count_id = models.ForeignKey(Counts, blank=True, on_delete=models.CASCADE)
