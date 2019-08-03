from __future__ import absolute_import, unicode_literals

from celery import  shared_task
from django.core.mail import get_connection


@shared_task
def send_bulk_emails(emails):
    """task for  sending emails in bulk

    args: emails

    return: string
    """
    connection = get_connection()
    connection.send_messages(emails)

    return f'{len(emails)} email(s) have been successfully sent'


@shared_task
def sample_task(a, b):
    return f'result of addition is {a + b}'
