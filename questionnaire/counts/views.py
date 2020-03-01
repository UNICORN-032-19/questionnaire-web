from rest_framework import viewsets
from questionnaire.counts.models import Counts, IN_PROGRESS_STATE, DONE_STATE
from questionnaire.users.models import User
from questionnaire.useranswers.models import UserAnswers
from django.http import HttpResponse
import json


class CountsViewset(viewsets.ViewSet):
    queryset = Counts.objects.all()
    permission_classes = ()

    def create(self, request):
        user = request.user
        if user:
            counts = Counts.objects.filter(user_id=user, state=IN_PROGRESS_STATE)[:1]
            if not counts:
                new_count = UserAnswers.objects.filter(user_id=user).count() + 1
                count_name = "Count #"+str(new_count)
                count = Counts(user_id=user, name=count_name)
                count.save()
            else:
                count = counts[0]
            return HttpResponse(json.dumps({"count_id": count.id, "count_name": count.name}))
        else:
            return HttpResponse(json.dumps({"error": "User not Found"}))

    def put(self, request, pk=None):
        count = Counts.objects.get(pk=pk)
        if count:
            count.state = DONE_STATE
            count.save()
