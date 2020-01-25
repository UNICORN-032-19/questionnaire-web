from django.db import models

# Create your models here.

class Answer(models.Model):
    # quiestion_id = models.PositiveIntegerField(primary_key=True)
    description = models.CharField(max_length=200)
    is_correct = models.Field.blank(default=False)
