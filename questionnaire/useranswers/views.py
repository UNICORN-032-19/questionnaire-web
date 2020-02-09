from django.shortcuts import render
from rest_framework import viewsets, serializers
from questionnaire.questions.models import Questions
from questionnaire.answers.models import Answers
from questionnaire.counts.models import Counts
from questionnaire.users.models import User
from questionnaire.useranswers.models import UserAnswers
from django.http import HttpResponse


class UserAnswersSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()
    count_id = serializers.IntegerField()


class UserAnswersViewSet(viewsets.GenericViewSet):
    queryset = UserAnswers.objects.all()
    serializer_class = UserAnswersSerializer
    permission_classes = ()


    # def list(self, request):
    #     return HttpResponse(json.dumps([]))

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            question_id = data["question_id"]
            answer_id = data["answer_id"]
            count_id = data["count_id"]
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
        return HttpResponse("Received invalid data")


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
