"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

import uuid
from django.db import models, transaction, IntegrityError
from django.utils.translation import gettext_lazy as _

from common_library.fields import UlidField


# Separation of Concerns
class TimestampedBaseModel(models.Model):
    """
    Abstract base model that provides timestamp fields for tracking
    creation and modification times of model instances.

    Fields:
        created_time (datetime): Timestamp when the object was created.
        modified_time (datetime): Timestamp when the object was last modified.
    """

    class Meta:
        abstract = True

    created_time = models.DateTimeField(
        verbose_name=_("created time"), auto_now_add=True
    )
    modified_time = models.DateTimeField(verbose_name=_("modified time"), auto_now=True)


class TimestampedULIDBaseModel(TimestampedBaseModel):
    """
    Abstract base model that extends TimestampedBaseModel by adding a
    unique public_key for external/public identification.

    Fields:
        public_key (str): A unique, externally usable identifier (UUID-based).

    Methods:
        get_by_public_key(key): Retrieve an instance by its public_key.
        set_public_key(max_retry): Assign a unique public_key if not already set.
        save(): Override save to ensure a valid unique public_key is generated.
    """

    class Meta:
        abstract = True

    uid = UlidField()
