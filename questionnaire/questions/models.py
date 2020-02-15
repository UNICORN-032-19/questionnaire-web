from django.db import models


class Questions(models.Model):
    text = models.TextField()
    multiple_answers = models.BooleanField(default=False)
