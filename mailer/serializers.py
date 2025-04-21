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
from mailer.mongodb_models import MailEvent


class DumpMailEventSerializer(serializers.Serializer):
    """
    Serializer for converting MailEvent model instances to a simplified dictionary representation.

    It includes logic to conditionally exclude the 'redirect_to' field when the event type is not 'link-click'.
    """
    event_type = serializers.CharField()
    created_time = serializers.DateTimeField()
    modified_time = serializers.DateTimeField()
    redirect_to = serializers.URLField(required=False, allow_null=True) # dynamic

    def to_representation(self, instance):
        """
        Customize the representation of the MailEvent instance to exclude 'redirect_to'
        if the event type is not 'link-click'.

        Args:
            instance: The MailEvent instance to be serialized.

        Returns:
            dict: The serialized data with 'redirect_to' excluded for non-link-click events.
        """
        ret = super().to_representation(instance)
        if ret.get('event_type') != MailEvent.LINK_CLICK:
            ret.pop('redirect_to', None)
        return ret


class MailEventSerializer(serializers.Serializer):
    """
    Serializer for validating and serializing mail event data when creating or updating a Mail instance.

    This serializer is used for creating new MailEvent records and validating their input.
    """
    name = serializers.ChoiceField(required=True, choices=MailEvent.event_type_choices)


class MailSerializer(serializers.ModelSerializer):
    """
    Serializer for handling Mail model instances, including serialization and deserialization
    of associated MailEvent data.

    This serializer is responsible for representing Mail instances and handling the creation
    of associated MailEvent records.
    """
    status = serializers.SerializerMethodField()
    events_list = MailEventSerializer(many=True, required=False)  # input for creating events
    events = serializers.SerializerMethodField()  # output, representing associated events

    class Meta:
        model = Mail
        fields = '__all__'
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

    def get_events(self, obj):
        """
        Get all MailEvent records associated with the current Mail instance.

        Args:
            obj: The Mail instance being serialized.

        Returns:
            list: A list of serialized MailEvent data for the associated Mail instance.
        """
        objects = MailEvent.objects.filter(sql_mail_id=obj.id).all()
        data = DumpMailEventSerializer(objects, many=True).data
        return data

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
        events_data = validated_data.pop('events_list', [])
        mail = super().create(validated_data)

        # If no events are provided, default to an 'open' event
        events_data = events_data if len(events_data) > 0 else [{'name': 'open'}]

        for event in events_data:
            event_type = event['name']
            payload = {
                "event_type": event_type,
                "sql_mail_id": mail.id
            }
            if event_type == MailEvent.LINK_CLICK:
                payload["redirect_to"] = "https://fake.ir"  # Example URL for link-click events

            event_object = MailEvent(**payload)
            event_object.save()

        return mail
