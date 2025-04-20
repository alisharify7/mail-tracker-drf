from django.contrib import admin

from attachments.models import Attachment, AttachmentType

admin.site.register(Attachment)
admin.site.register(AttachmentType)
