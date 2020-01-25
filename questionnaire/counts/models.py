from django.db import models

# Create your models here.
from django.db import models


class Counts(models.Model):
    names = models.CharField(max_length=200)

