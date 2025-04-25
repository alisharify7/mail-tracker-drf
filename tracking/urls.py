from django.urls import path
from . import views

urlpatterns = [
    path('<str:event_key>', views.WebHockAPIView.as_view(), name='web-hock'),
]
