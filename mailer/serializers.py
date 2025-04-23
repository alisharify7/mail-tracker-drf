"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""
from random import choices

from rest_framework import serializers

from mailer.models import Mail, CarbonCopy
from mailer.mongodb_models import MailEvent
from attachments.serializers import Attachment, AttachmentSerializer

class MailEventSerializer(serializers.Serializer):
    """
    Serializer for validating and serializing mail event data when creating or updating a Mail instance.

    This serializer is used for creating new MailEvent records and validating their input.
    """

    type = serializers.ChoiceField(required=True, source="event_type", choices=MailEvent.event_type_choices)
    redirect_to = serializers.URLField(required=False)

    class Meta:
        fields = ("type",)
        read_only_fields = ("type",)


    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get("type") != MailEvent.LINK_CLICK:
            ret.pop("redirect_to", None)
        return ret


class AttachmentRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        # Serialize the related Attachment instance using AttachmentSerializer
        return AttachmentSerializer(value).data

class CarbonCopySerializer(serializers.Serializer):
    email_address = serializers.EmailField()


class MailSerializer(serializers.ModelSerializer):
    """
    Serializer for handling Mail model instances, including serialization and deserialization
    of associated MailEvent data.

    This serializer is responsible for representing Mail instances and handling the creation
    of associated MailEvent records.
    """

    status = serializers.SerializerMethodField()
    events = MailEventSerializer(many=True, required=False)

    attachments = AttachmentRelatedField(
        many=True,
        queryset=Attachment.objects.all()
    )
    carbon_copies = CarbonCopySerializer(
        many=True,
    )

    class Meta:
        model = Mail
        fields = "__all__"
        read_only_fields = ["created_time", "modified_time", "public_key", "id"]

    def get_status(self, obj):
        """
        Get the status display of the Mail instance.

        Args:
            obj: The Mail instance being serialized.

        Returns:
            str: The status display of the Mail instance.
        """
        return obj.get_status_display()



    def create(self, validated_data):
        """
        Override the default create method to handle creation of a Mail instance
        along with associated MailEvent records. If no events are provided, a default
        'open' event will be created.

        Args:
            validated_data: The validated input data for creating a Mail instance.

        Returns:
            Mail: The created Mail instance.
        """
        events_data = validated_data.pop("events", [])
        carbon_copies = validated_data.pop("carbon_copies", [])
        mail = super().create(validated_data)

        for carbon in carbon_copies:
            print(carbon)
            carbon = CarbonCopy.objects.create(mail=mail, email_address=carbon["email_address"])


        # If no events are provided, default to an 'open' event
        events_data = events_data if len(events_data) > 0 else [{"event_type": "open"}]
        event_list = []
        for event in events_data:
            event_type = event["event_type"]
            payload = {"event_type": event_type, "sql_mail_id": mail.id}
            if event_type == MailEvent.LINK_CLICK:
                payload["redirect_to"] = (
                    "https://fake.ir"  # Example URL for link-click events
                )

            event_object = MailEvent(**payload)
            event_object.save()
            event_list.append(event_object)

        mail.events = event_list
        return mail
