from django.db import models

# Create your models here.

class Questions(models.Model):
    text = models.PositiveIntegerField(primary_key=True)
    #answers_id =