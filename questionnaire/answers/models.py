from django.db import models
from questionnaire.questions.models import Questions


class Answers(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=False)
    description = models.TextField()
    is_correct = models.BooleanField()
