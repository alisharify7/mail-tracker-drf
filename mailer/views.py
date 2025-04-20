"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from mailer.models import Mail
from mailer.serializers import MailSerializer


class ListCreateMailView(ListCreateAPIView):
    serializer_class = MailSerializer
    queryset = Mail.objects.all()

class RetrieveDestroyViewMailView(RetrieveDestroyAPIView):
    serializer_class = MailSerializer
    queryset = Mail.objects.all()