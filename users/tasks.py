from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_reset_password(subject, message, from_email, recipient_list, **kwargs):
    send_mail(subject, message, from_email, recipient_list, **kwargs)