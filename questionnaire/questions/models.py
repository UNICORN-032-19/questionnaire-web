from django.db import models


class Questions(models.Model):
    text = models.PositiveIntegerField(primary_key=True)
    #answers_id =

