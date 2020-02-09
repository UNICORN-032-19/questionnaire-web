from django.shortcuts import render
from questionnaire.counts.models import Counts
from questionnaire.users.models import User
from django.http import HttpResponse


# Create your views here.
def count_new(request):
    user_id = request.POST.get("user_id")
    user = User.objects.filter(id=user_id)[0]
    count = Counts(user_id=user, name="test")
    count.save()
    return HttpResponse(str(count.id))
