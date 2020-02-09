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
    questions = Answers.get_formatted_questions()
    return render(request, 'questions.html', context={"questions": questions})


def save_question(request):
    question_id = int(request.POST.get("question_id"))
    answer_id = int(request.POST.get("answer_id"))
    question = Questions.objects.filter(id=question_id)[0]
    answer = Answers.objects.filter(id=answer_id)[0]
    # Dummy operations for get user/count
    user = User.objects.all()[0]
    count = Counts(user_id=user, name="test")
    count.save()
    obj = UserAnswers(question_id=question, answer_id=answer, count_id=count, user_id=user)
    obj.save()
    return HttpResponse(str(obj.id))



