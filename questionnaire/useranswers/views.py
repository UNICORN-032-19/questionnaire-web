from django.shortcuts import render
from questionnaire.counts.models import Counts
from questionnaire.users.models import User
from questionnaire.useranswers.models import UserAnswers
from django.http import HttpResponse


def results(request):
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
            "answer": obj.answer_id.description,
            "is_correct": obj.answer_id.is_correct,
        }]
    return render(request, 'results.html', context={"results": results})
