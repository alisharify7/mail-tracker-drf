from django.db.models.signals import post_delete
from django.dispatch import receiver

from attachments.models import Attachment


@receiver(post_delete, sender=Attachment)
def delete_attachments(sender, instance, **kwargs):
    """delete attachments file from AWS s3 after deletion"""
    if instance.file:
        instance.file.delete()
