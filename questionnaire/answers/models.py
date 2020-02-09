from django.db import models
from questionnaire.questions.models import Questions


class Answers(models.Model):
    question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=False)
    description = models.TextField()
    is_correct = models.BooleanField()


    @classmethod
    def get_formatted_answers(cls, question_id):
        result = []
        for answer in cls.objects.filter(question_id=question_id):
            result += [{"id": answer.id, "description": answer.description}] 
        return result

    @classmethod
    def get_formatted_questions(cls):
        result = []
        for question in Questions.objects.all():
            result += [{
                "id": question.id,
                "text": question.text,
                "answers": cls.get_formatted_answers(question.id),
            }]
        return result
