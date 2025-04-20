"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

from django.urls import path
from attachments import views

urlpatterns = [
    path(
        "<int:pk>/",
        views.RetrieveDestroyAttachmentView.as_view(),
        name="retrieve-delete-attachment",
    ),
    path("", views.ListCreateAttachmentView.as_view(), name="create-list-attachment"),
]
