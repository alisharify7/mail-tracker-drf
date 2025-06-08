from rest_framework.views import APIView
from mailer.mongodb_models import MailEvent
from mailer.models import Mail


class WebHockAPIView(APIView):
    def get(self, request, event_key: str):
        """render pixel for tracking"""
        print(event_key)
        pass
