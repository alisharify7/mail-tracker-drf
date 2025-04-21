"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

import datetime
from mongoengine import Document, ObjectIdField, StringField, IntField, URLField, DateTimeField

class MailEvent(Document):
    """MongoDB Collection definition for Mail Events"""

    _id = ObjectIdField(primary_key=True)
    event_type = StringField(required=True, choices=["open", "link-click"])
    sql_mail_id = IntField(required=True)
    redirect_to = URLField(required=False, null=True)
    created_time = DateTimeField(default=lambda: datetime.datetime.now(datetime.UTC))
    modified_time = DateTimeField(default=lambda: datetime.datetime.now(datetime.UTC))

    def save(self, *args, **kwargs):
        self.modified_time = datetime.datetime.now(datetime.UTC)
        return super().save(*args, **kwargs)

    def _save_update(self, *args, **kwargs):
        self.modified_time = datetime.datetime.now(datetime.UTC)
        super()._save_update(*args, **kwargs)

    def clean(self):
        if self.event_type != "link-click":
            self.redirect_to = None