from django.core.management.base import BaseCommand, CommandError
from questionnaire.questions.models import Questions
from questionnaire.answers.models import Answers


class Command(BaseCommand):
    help = 'List Questions with correct answers'

    # def add_arguments(self, parser):
    #     parser.add_argument('listall', nargs='+', type=bool)

    def handle(self, *args, **options):
        # try:
        #     questions = Questions.objects.all()
        # except Poll.DoesNotExist:
        #     raise CommandError('Poll "%s" does not exist' % poll_id)
        questions = Questions.objects.all()
        for question in questions:
            correct_answers = Answers.objects.filter(question_id=question.id, is_correct=True)
            answer = "|".join([x.description for x in correct_answers])
            self.stdout.write(
                self.style.SUCCESS('Question #%s(%s): %s - ' % (
                        question.id, question.multiple_answers, question.text
                    )
                ) + self.style.WARNING(answer)
            )
