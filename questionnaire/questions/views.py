from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import Questions


class QuestionViewSet(viewsets.GenericViewSet):
    """
    Updates and retrieves questions
    """
    queryset = Questions.objects.all()
    # serializer_class = QuestionSerializer
    permission_classes = ()
