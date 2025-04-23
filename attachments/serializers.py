"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

from rest_framework import serializers

from attachments.models import Attachment, AttachmentType


class AttachmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachmentType
        fields = ["main_type", "sub_type"]


class AttachmentSerializer(serializers.ModelSerializer):
    attachment_type = AttachmentTypeSerializer(required=False)

    class Meta:
        model = Attachment
        fields = "__all__"
        read_only_fields = [
            "created_time",
            "modified_time",
            "public_key",
            "id",
            "attachment_type",
        ]
