from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from questionnaire.questions.models import Questions
from questionnaire.answers.models import Answers
from questionnaire.counts.models import Counts
from questionnaire.users.models import User
from django.http import HttpResponse
import json
from questionnaire.useranswers.models import UserAnswers 


class QuestionViewSet(viewsets.GenericViewSet):
    """
    Updates and retrieves questions
    """
    queryset = Questions.objects.all()
    # serializer_class = QuestionSerializer
    permission_classes = ()

def questions(request):
    users = User.objects.all()
    questions = Answers.get_formatted_questions()
    return render(request, 'questions.html', context={"questions": questions, "users": users})


def save_question(request):
    question_id = int(request.POST.get("question_id"))
    answer_id = int(request.POST.get("answer_id"))
    count_id = int(request.POST.get("count_id"))
    question = Questions.objects.filter(id=question_id)[0]
    answer = Answers.objects.filter(id=answer_id)[0]
    count = Counts.objects.filter(id=count_id)[0]
    exists  = UserAnswers.objects.filter(question_id=question, count_id=count, user_id=count.user_id)
    if exists:
        obj = exists[0]
        obj.answer_id = answer
    else:
        obj = UserAnswers(question_id=question, answer_id=answer, count_id=count, user_id=count.user_id)
    obj.save()
    return HttpResponse(str(obj.id))
