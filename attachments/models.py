"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

import mimetypes
import os
import uuid
from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from common_library.model import TimestampedULIDBaseModel, TimestampedBaseModel


class AttachmentType(TimestampedBaseModel):
    """
    Represents a type or category for an attachment.

    This model is used to categorize attachments into different types, such as
    'image', 'document', 'video', etc. It helps organize and manage various
    attachment formats in the system.

    Fields:
        name (str): The name of the attachment type (e.g., 'image', 'pdf', etc.).

    Methods:
        __str__(): Returns the name of the attachment type as a string.
    """

    class Meta:
        verbose_name = _("Attachment Type")
        verbose_name_plural = _("Attachment Types")
        unique_together = ("main_type", "sub_type")

    # image, video, application
    main_type = models.CharField(
        verbose_name=_("main_type"), max_length=256, blank=False, null=False
    )

    # jpeg, png, pdf
    sub_type = models.CharField(
        verbose_name=_("sub_type"), max_length=256, blank=False, null=False
    )

    def __str__(self):
        return f"{self.main_type}/{self.sub_type}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.main_type!r}, {self.sub_type!r})"


def attachment_upload_to(instance, filename):
    """
    Generate upload path: attachments/%Y/%m/%d/<uuid4>.<extension>
    """
    base, ext = os.path.splitext(filename)

    new_filename = f"{uuid.uuid4().hex}{ext}"

    date_path = datetime.now().strftime("%Y/%m/%d")

    return f"attachments/{date_path}/{new_filename}"


class Attachment(TimestampedULIDBaseModel):
    """
    Represents a file attachment associated with an email or any other entity.

    Fields:
        name (str): A human‑readable name for the attachment.
        file (FileField): The actual file, stored under MEDIA_ROOT/attachments/YYYY/MM/DD/.
        created_time (datetime): Timestamp when this attachment was first created.
        modified_time (datetime): Timestamp when this attachment was last modified.
    """

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    name = models.CharField(_("name"), max_length=255)
    file = models.FileField(
        _("file"),
        upload_to=attachment_upload_to,
        max_length=1024,
    )

    attachment_type = models.ForeignKey(
        AttachmentType,
        verbose_name=_("Attachment Type"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attachments",
    )

    def delete(self, *args, **kwargs):
        """
        Deletes the attachment instance, ensuring that the associated file is also removed from storage (e.g., S3).

        This method overrides the default `delete()` method to ensure the file is deleted before removing the record
        from the database.

        Args:
            *args: Positional arguments to be passed to the parent's `delete()` method.
            **kwargs: Keyword arguments to be passed to the parent's `delete()` method.
        """
        # if self.file: # Moved to signals sections
        #     self.file.delete()  # Deletes the file from storage (S3, local, etc.)
        super().delete(
            *args, **kwargs
        )  # Call the parent delete method to remove the record from the database

    def save(self, *args, **kwargs):
        """
        Saves the attachment instance. If the file is provided but the attachment type is not set,
        it will infer the type based on the file's MIME type (e.g., image/jpeg -> image, jpeg).

        Args:
            *args: Positional arguments to be passed to the parent's `save()` method.
            **kwargs: Keyword arguments to be passed to the parent's `save()` method.
        """
        if self.file and not self.attachment_type:
            mime_type, _ = mimetypes.guess_type(self.file.name)
            if mime_type:
                main_type, sub_type = mime_type.split("/")
                attachment_type, _ = AttachmentType.objects.get_or_create(
                    main_type=main_type,
                    sub_type=sub_type,
                )
                self.attachment_type = attachment_type

        super().save(*args, **kwargs)
