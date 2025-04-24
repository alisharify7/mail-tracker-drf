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

    def perform_create(self, serializer):
        mail = serializer.save()
        payload = {
            "subject": mail.subject,
            "body": mail.body,
            "recipient": mail.recipient,
        }
        if mail.scheduled_time:
            return send_email.apply_async(
                args=(payload, mail.id),
                eta=mail.scheduled_time,
            )
        return send_email.delay(
            message=payload,
            object_id=mail.id,
        )


class RetrieveDestroyViewMailView(RetrieveDestroyAPIView):
    serializer_class = MailSerializer
    queryset = Mail.objects.all()
