from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from config.celery import app


@app.task
def send_confirmation_code(email, confirmation_code):
    html_message = render_to_string(
        'booking/code_mail.html', 
        {'confirmation_code': confirmation_code}   
        )
    send_mail(
        'Confirm your booking!',
        '',
        settings.EMAIL_HOST_USER,
        {email},
        html_message=html_message,
        fail_silently=False
    )