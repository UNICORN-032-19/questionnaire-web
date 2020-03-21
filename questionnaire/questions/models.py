from django.db import models
from taggit.managers import TaggableManager


class QuestionManager(models.Manager):
    def answers(self):
        from questionnaire.answers.models import Answers
        answers = Answers.objects.filter(question_id=self.id)


class Questions(models.Model):
    objects = QuestionManager()
    text = models.TextField()
    multiple_answers = models.BooleanField(default=False)
    tags = TaggableManager()

    def answers_objects(self):
        from questionnaire.answers.models import Answers
        return Answers.objects.filter(question_id=self.id)
