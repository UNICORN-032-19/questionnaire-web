from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from questionnaire.questions.models import Questions
from questionnaire.answers.models import Answers


class QuestionViewSet(viewsets.GenericViewSet):
    """
    Updates and retrieves questions
    """
    queryset = Questions.objects.all()
    # serializer_class = QuestionSerializer
    permission_classes = ()

def questions(request):
    results = []
    questions = Questions.objects.all()
    for question in questions:
        answers = Answers.objects.filter(quiestion_id=question.id)
        results += [{"q": question.text, "answers": [x.description for x in answers]}]
    return render(request, 'questions.html', context={"results": results})
