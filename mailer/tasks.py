from celery import shared_task


@shared_task(max_retries=5, default_retry_delay=10)
def send_email(obj):
    print("Sending email")
