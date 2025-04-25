"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

import datetime
from mongoengine import (
    Document,
    ObjectIdField,
    StringField,
    IntField,
    URLField,
    DateTimeField, ReferenceField, DictField, BooleanField,
)


class MailEvent(Document):
    """MongoDB Collection definition for Mail Events"""

    meta = {"db_alias": "default"}

    LINK_CLICK = "link-click"
    OPEN = "open"
    event_type_choices = [OPEN, LINK_CLICK]

    event_type = StringField(required=True, choices=event_type_choices)
    sql_mail_id = IntField(required=True)
    redirect_to = URLField(required=False)
    created_time = DateTimeField(default=lambda: datetime.datetime.now(datetime.UTC))
    modified_time = DateTimeField(default=lambda: datetime.datetime.now(datetime.UTC))

    def save(self, *args, **kwargs):
        self.modified_time = datetime.datetime.now(datetime.UTC)
        return super().save(*args, **kwargs)

    def _save_update(self, *args, **kwargs):
        self.modified_time = datetime.datetime.now(datetime.UTC)
        super()._save_update(*args, **kwargs)


class MailEventLog(Document):
    """MongoDB Collection definition for Mail Events"""

    meta = {
        "db_alias": "default",
        "indexes": [
            "event",
            "ip_address",
            "created_time",
            "is_bot",
        ]
    }

    event = ReferenceField(MailEvent, required=True)

    user_agent = StringField(required=True)
    browser = StringField()
    os = StringField()
    device_type = StringField()  # e.g., mobile, desktop, tablet
    ip_address = StringField(required=True)
    geo_location = DictField()  # e.g., {"country": "IR", "city": "Tehran"}

    is_bot = BooleanField(default=False)
    referrer = StringField()

    created_time = DateTimeField(default=lambda: datetime.datetime.now(datetime.UTC))
    modified_time = DateTimeField(default=lambda: datetime.datetime.now(datetime.UTC))

    def save(self, *args, **kwargs):
        self.modified_time = datetime.datetime.now(datetime.UTC)
        return super().save(*args, **kwargs)

    def _save_update(self, *args, **kwargs):
        self.modified_time = datetime.datetime.now(datetime.UTC)
        super()._save_update(*args, **kwargs)

