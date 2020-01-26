from django.db import models
from questionnaire.users.models import User
from questionnaire.counts.models import Counts


class Scores(models.Model):
    count_id = models.ForeignKey(Counts, blank=True, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    result = models.CharField(max_length=200)
