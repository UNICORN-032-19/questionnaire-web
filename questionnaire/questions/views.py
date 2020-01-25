from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny


class QuestionViewSet(viewsets.GenericViewSet):
    """
    Updates and retrieves questions
    """
    # queryset = Question.objects.all()
    # serializer_class = QuestionSerializer
    permission_classes = (,)

