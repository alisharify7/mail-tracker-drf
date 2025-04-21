from celery import shared_task, Task
from django.core.mail import send_mail
from mailer.models import Mail
from django.conf import settings


@shared_task(bind=True, max_retries=5, default_retry_delay=10)
def send_email(self: Task, message, obj_id):
    try:
        obj = Mail.objects.get(id=obj_id)
    except Mail.DoesNotExist:
        return None

    result = send_mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        subject=message["subject"],
        html_message=message["body"],
        recipient_list=message["recipient"],
        fail_silently=True,
    )
    print(f"Sending email {result}")
