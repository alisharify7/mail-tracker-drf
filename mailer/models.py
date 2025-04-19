"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class Mail(models.Model):
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

    class Meta:
        db_table = "mail"
        verbose_name = _("Mail")
        verbose_name_plural = _("Mails")

    subject = models.CharField(
        verbose_name=_("subject"), max_length=256, blank=False, null=False
    )
    body = models.CharField(
        verbose_name=_("body"), max_length=8096, blank=False, null=False
    )
    recipient = models.EmailField(
        verbose_name=_("recipient"), max_length=254, blank=False, null=False
    )
    scheduled_time = models.DateTimeField(
        verbose_name=_("scheduled time"), blank=True, null=True
    )
    created_time = models.DateTimeField(
        verbose_name=_("created time"), auto_now_add=True
    )
    modified_time = models.DateTimeField(verbose_name=_("modified time"), auto_now=True)
    public_key = models.CharField(
        verbose_name=_("public key"),
        max_length=32,
        blank=False,
        null=False,
        unique=True,
    )

    tags = TaggableManager()

    def set_public_key(self, max_retry: int = 10) -> bool:
        """
        Generates a unique public_key and assigns it to the instance.

        Args:
            max_retry (int): Maximum number of attempts to find a unique key.

        Returns:
            bool: True if a unique key was found and assigned, False otherwise.
        """
        for _ in range(max_retry):
            key = uuid.uuid4().hex
            if not self.__class__.objects.filter(public_key=key).exists():
                self.public_key = key
                return True
        return False

    def __str__(self):
        return f"{self.pk}-{self.subject}"


class CarbonCopy(models.Model):
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
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created time")
    )
    modified_time = models.DateTimeField(auto_now=True, verbose_name=_("modified time"))

    class Meta:
        db_table = "carbon_copy"
        verbose_name = _("Carbon Copy")
        verbose_name_plural = _("Carbon Copies")

    def __str__(self):
        return f"{self.email_address} (Mail #{self.mail_id})"
