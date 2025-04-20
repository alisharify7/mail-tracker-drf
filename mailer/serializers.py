"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

from rest_framework import serializers

from mailer.models import Mail


class MailSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Mail
        fields = '__all__'
        read_only_fields = ["created_time", "modified_time", "public_key", "id"]

    def get_status(self, obj):
        return obj.get_status_display()
