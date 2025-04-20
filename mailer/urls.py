"""
* mail-tracker-drf
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2025 - ali sharifi
* https://github.com/alisharify7/mail-tracker-drf
"""

from django.urls import path
from mailer import views


urlpatterns = [
    path("", views.ListCreateMailView.as_view(), name="list-create-mail"),
    path("<int:pk>/", views.RetrieveDestroyViewMailView.as_view(), name="retrieve-delete-mail"),
]
