from django.shortcuts import render
from rest_framework import viewsets, serializers
from questionnaire.questions.models import Questions
from questionnaire.answers.models import Answers
from questionnaire.counts.models import Counts
from questionnaire.users.models import User
from questionnaire.useranswers.models import UserAnswers
from django.http import HttpResponse
import json


class UserAnswersSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.ListField(child=serializers.IntegerField(), allow_empty=True, min_length=0, max_length=10)
    count_id = serializers.IntegerField()


class UserAnswersViewSet(viewsets.GenericViewSet):
    queryset = UserAnswers.objects.all()
    serializer_class = UserAnswersSerializer
    permission_classes = ()


    def list(self, request):
        objects = UserAnswers.objects.all().order_by('user_id', 'count_id')
        results = {}
        for obj in objects:
            username = obj.user_id.username
            count_id = obj.count_id.id
            if username not in results:
                results[username] = {}
            if count_id not in results[username]:
                results[username][count_id] = []
            results[username][count_id] += [{
                "text": obj.question_id.text,
                "answer": [x["description"] for x in obj.answer_id.values()],
                "is_correct": all([x["is_correct"] for x in obj.answer_id.values()]),
            }]
        return HttpResponse(json.dumps(results))

    def create(self, request):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            data = serializer.validated_data
            question_id = data["question_id"]
            answer_id = data["answer_id"]
            count_id = data["count_id"]
            question = Questions.objects.get(pk=question_id)
            answer = [Answers.objects.get(pk=a) for a in answer_id]
            count = Counts.objects.get(pk=count_id)
            exists  = UserAnswers.objects.filter(question_id=question, count_id=count, user_id=count.user_id)
            if exists:
                obj = exists[0]
            else:
                obj = UserAnswers(question_id=question, count_id=count, user_id=count.user_id)
            obj.save()
            obj.answer_id.set(answer)
            obj.save()
            return HttpResponse(str(obj.id))
        return HttpResponse("Received invalid data")
