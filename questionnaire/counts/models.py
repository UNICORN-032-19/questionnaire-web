from django.db import models
from questionnaire.users.models import User


class Counts(models.Model):
    user_id = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
