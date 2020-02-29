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
from django.contrib.auth.decorators import login_required


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField()


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    answers = serializers.SerializerMethodField()
    multiple_answers = serializers.BooleanField()

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
        current_count = int(request.GET.get("current_count", 0))
        if not current_count:
            return HttpResponse(status=400, content=json.dumps({"error": "Count not specified"}))
        serializer = self.serializer_class()
        questions = [serializer.to_representation(x) for x in self.queryset]
        answered = UserAnswers.objects.filter(user_id=request.user, count_id=Counts.objects.get(pk=current_count))
        answered = {x.question_id.id: [y["id"] for y in x.answer_id.values()] for x in answered}
        result = {"questions": questions, "answered": answered}
        return HttpResponse(json.dumps(result))


@login_required
def questions(request):
    return render(request, 'questions.html')
