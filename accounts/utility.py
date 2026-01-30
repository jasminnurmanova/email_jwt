from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import re

def send_simple_email(user,code):
    subject = "Tasdiqlash kodingiz"
    message = f"Sizning kodingiz: {code}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user, ]

    send_mail(subject,message, from_email,recipient_list)

    return True

email_regex=re.compile("^[A-Za-z0-9._%+-]+@gmail\.com$")

def check_email(email):
    if re.fullmatch(email_regex,email):
        email = True
    else:
        raise ValidationError("Email xato kiritilgan")

    return email
