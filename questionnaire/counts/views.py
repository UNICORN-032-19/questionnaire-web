from rest_framework import viewsets
from questionnaire.counts.models import Counts
from questionnaire.users.models import User
from questionnaire.useranswers.models import UserAnswers
from django.http import HttpResponse
import json


class CountsViewset(viewsets.ViewSet):
    queryset = Counts.objects.all()
    # serializer_class = QuestionSerializer
    permission_classes = ()

    def create(self, request):
        user_id = self.request.data.get("user_id")
        user = User.objects.filter(id=user_id)
        if user:
            user = user[0]
            current_count = UserAnswers.objects.filter(user_id=user).count() + 1
            count_name = "Count #"+str(current_count)
            count = Counts(user_id=user, name=count_name)
            count.save()
            return HttpResponse(json.dumps({"count_id": count.id, "count_name": count_name}))
        else:
            return HttpResponse(json.dumps({"error": "User not Found"}))
