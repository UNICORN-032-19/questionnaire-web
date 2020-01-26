from django.db import models


class Scores(models.Model):
    count = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    result = models.CharField(max_length=200)
