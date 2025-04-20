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
    modified_time = models.DateTimeField(
        verbose_name=_("modified time"), auto_now=True
    )


class TimestampedUUIDBaseModel(TimestampedBaseModel):
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

    public_key = models.CharField( # UUIDField
        verbose_name=_("public key"),
        max_length=32,
        blank=False,
        null=False,
        unique=True,
    )

    @classmethod
    def get_by_public_key(cls, key):
        """
        Retrieves an object instance by its public_key.

        Args:
            key (str): The public_key to search for.

        Returns:
            Instance of the model if found, otherwise raises DoesNotExist.
        """
        return cls.objects.get(public_key=key)

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

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure a unique public_key is assigned
        before saving the object. Uses transaction.atomic and handles potential
        race conditions with retry logic.

        Raises:
            ValueError: If a unique public_key cannot be generated after max retries.
        """
        if not self.public_key:
            for _ in range(10):
                self.set_public_key()
                try:
                    with transaction.atomic():
                        return super().save(*args, **kwargs)
                except IntegrityError:
                    continue
            raise ValueError("Failed to generate unique public key after multiple retries")
        return super().save(*args, **kwargs)
