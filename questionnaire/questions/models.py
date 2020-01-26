from django.db import models


class Questions(models.Model):
    text = models.TextField()
