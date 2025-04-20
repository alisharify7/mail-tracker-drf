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


class AttachmentType(models.Model):
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

    # image, video, application
    main_type = models.CharField(
        verbose_name=_("main_type"), max_length=256, blank=False, null=False
    )

    # jpeg, png, pdf
    sub_type = models.CharField(
        verbose_name=_("sub_type"), max_length=256, blank=False, null=False
    )

    class Meta:
        verbose_name = _("Attachment Type")
        verbose_name_plural = _("Attachment Types")
        unique_together = ("main_type", "sub_type")

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


class Attachment(models.Model):
    """
    Represents a file attachment associated with an email or any other entity.

    Fields:
        name (str): A human‑readable name for the attachment.
        file (FileField): The actual file, stored under MEDIA_ROOT/attachments/YYYY/MM/DD/.
        created_time (datetime): Timestamp when this attachment was first created.
        modified_time (datetime): Timestamp when this attachment was last modified.
    """

    name = models.CharField(_("name"), max_length=255)
    file = models.FileField(
        _("file"),
        upload_to=attachment_upload_to,
        max_length=1024,
    )
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    attachment_type = models.ForeignKey(
        AttachmentType,

        if self.file and not self.attachment_type:

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
        """
        Uploads the given file object to the specified S3-compatible bucket
        (e.g., Arvan S3) and updates this instance's `file` URL accordingly.

        This method should be implemented only if the default Django storage
        backend does not work with your S3 provider.

        Args:
            file_obj (File): Open file-like object to upload (e.g., InMemoryUploadedFile).
            bucket (str): The name of the S3 bucket.
            key (str): The object key (path) under which to store the file.

        Returns:
            str: The full URL of the uploaded file, which should then be saved
                 into `self.file.name` or returned for later assignment.
        """
        # import boto3
        # s3 = boto3.client(
        #     "s3",
        #     aws_access_key_id=...,
        #     aws_secret_access_key=...,
        #     region_name=...,
        #     endpoint_url="https://s3.ir-thr-at1.arvanstorage.com"  # Arvan endpoint
        # )
        # s3.upload_fileobj(file_obj, bucket, key)
        # url = f"https://{bucket}.s3.ir-thr-at1.arvanstorage.com/{key}"
        # self.file.name = key  # so that file.url returns the right path
        # self.save(update_fields=["file", "modified_time"])
        # return url

        raise NotImplementedError("upload_and_set_url must be implemented")
