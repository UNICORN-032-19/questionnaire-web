from django.db import models

# Create your models here.


app_label = "common"


class UserAnswers(models.Model):
    user_id = models.CharField(max_length=200)
    question_id = models.CharField(max_length=200)
    answer_id = models.CharField(max_length=200)
    count_id = models.CharField(max_length=200)
