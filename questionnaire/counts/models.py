from django.db import models
from questionnaire.users.models import User


IN_PROGRESS_STATE = 1
DONE_STATE = 2

STATE_CHOICES = (
    (IN_PROGRESS_STATE, "In Progress"),
    (DONE_STATE, "Done"),
)


class Counts(models.Model):
    user_id = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    state = models.IntegerField(choices=STATE_CHOICES, default=IN_PROGRESS_STATE)
