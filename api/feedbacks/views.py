from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.feedbacks.serializers import FeedbacksSerializer
from feedbacks.models import Feedback


class FeedbacksViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbacksSerializer
    permission_classes = [IsAuthenticated]
