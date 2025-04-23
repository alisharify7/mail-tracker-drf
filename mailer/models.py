"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


from taggit.managers import TaggableManager
from attachments.models import Attachment
from common_library.model import TimestampedUUIDBaseModel, TimestampedBaseModel


class Mail(TimestampedUUIDBaseModel):
    """
    Represents an email to be sent to a recipient.

    This model contains the essential data required for composing and scheduling an email, including:
    - subject and body of the email,
    - recipient's email address,
    - scheduled time for sending the email (optional),
    - timestamps for creation and modification,
    - a unique public_key for tracking or identifying the mail externally.

    Fields:
        subject (str): The subject of the email.
        body (str): The content/body of the email.
        recipient (str): The recipient's email address.
        scheduled_time (datetime): Optional time to schedule the email to be sent.
        created_time (datetime): Timestamp when the email object was created.
        modified_time (datetime): Timestamp for the last update to the email object.
        public_key (str): A unique public identifier (e.g., for tracking links).
    """

    PENDING = 1
    SENT = 2
    FAILED = 3
    UNKNOWN = 4
    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (SENT, _("Sent")),
        (FAILED, _("Failed")),
        (UNKNOWN, _("Unknown")),
    )

    class Meta:
        # db_table = "mail"
        verbose_name = _("Mail")
        verbose_name_plural = _("Mails")

    subject = models.CharField(
        verbose_name=_("subject"), max_length=256, blank=False, null=False
    )
    body = models.CharField(
        verbose_name=_("body"), max_length=8096, blank=False, null=False
    )
    recipient = models.EmailField(  # TODO: recipients can be a list :) instead of single recipient
        verbose_name=_("recipient"), max_length=254, blank=False, null=False
    )
    scheduled_time = models.DateTimeField(
        verbose_name=_("scheduled time"), blank=True, null=True
    )

    attachments = models.ManyToManyField(Attachment, related_name="mails", blank=True)

    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],
    )

    tags = TaggableManager()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(subject={self.subject!r}, body={self.body!r})"
        )

    def __str__(self):
        return f"MailObject {self.pk}-{self.subject}"


class CarbonCopy(TimestampedBaseModel):
    """
    Represents a CC recipient for an email.
    """

    email_address = models.EmailField(
        verbose_name=_("email address"), max_length=254, blank=False, null=False
    )
    mail = models.ForeignKey(
        Mail,
        verbose_name=_("mail"),
        on_delete=models.CASCADE,
        related_name="carbon_copies",
    )

    class Meta:
        # db_table = "carbon_copy"
        verbose_name = _("Carbon Copy")
        verbose_name_plural = _("Carbon Copies")

    def __str__(self):
        return f"{self.email_address} (Mail #{self.mail_id})"

    def __repr__(self):
        return f"{self.__class__.__name__}(email_address={self.email_address!r})"
