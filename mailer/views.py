"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from mailer.serializers import MailSerializer


class MailView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


