from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from questionnaire.questions.models import Questions
from questionnaire.answers.models import Answers
from questionnaire.counts.models import Counts
from questionnaire.users.models import User
from django.http import HttpResponse
import json
from questionnaire.useranswers.models import UserAnswers
import questionnaire.useranswers.views as ua_views


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField()


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    answers = serializers.SerializerMethodField()

    def get_answers(self, obj):
        serializer = AnswerSerializer()
        return [
            serializer.to_representation(x)
            for x in Answers.objects.filter(question_id=obj.id)
        ]


class QuestionViewSet(viewsets.GenericViewSet):
    """
    Updates and retrieves questions
    """
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = ()


    def list(self, request):
        serializer = self.serializer_class()
        result = [serializer.to_representation(x) for x in self.queryset]
        return HttpResponse(json.dumps(result))


def questions(request):
    users = User.objects.all()
    return render(request, 'questions.html', context={"users": users})
