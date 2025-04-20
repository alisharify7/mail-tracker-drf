"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from attachments.models import Attachment
from attachments.serializers import AttachmentSerializer


class CreateListAttachmentView(ListCreateAPIView):
    """Create a new attachment or list all attachments with pagination."""

    queryset = Attachment.objects.all().order_by("-created_time")
    serializer_class = AttachmentSerializer


class RetrieveDestroyAttachmentView(RetrieveDestroyAPIView):
    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()
    lookup_field = "public_key"
