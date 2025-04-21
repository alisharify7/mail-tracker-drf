"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

import datetime

from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from mailer.models import Mail
from mailer.serializers import MailSerializer
from mailer.tasks import send_email


class ListCreateMailView(ListCreateAPIView):
    serializer_class = MailSerializer
    queryset = Mail.objects.all()


class RetrieveDestroyViewMailView(RetrieveDestroyAPIView):
    serializer_class = MailSerializer
    queryset = Mail.objects.all()
