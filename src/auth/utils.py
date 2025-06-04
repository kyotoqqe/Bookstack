import json
import base64
import ssl
import smtplib 

from smtplib import SMTPException
from fastapi import HTTPException
from pathlib import Path
from email.message import EmailMessage

from src.config import settings
 
CONFIRM_EMAIL_TEMPLATE_PATH = Path(__file__).parent.parent.parent / "templates" / "confirmation_email.html"
PASSWORD_RESET_EMAIL_TEMPLATE_PATH = Path(__file__).parent.parent.parent / "templates" / "password_reset_email.html"

def generate_url_token(payload_json:str):
    base64_token = base64.urlsafe_b64encode(payload_json.encode())
    return base64_token.decode()

def decode_url_token(token:str):
    token_data = base64.urlsafe_b64decode(token)
    return json.loads(token_data)

def send_confirmation_email(receiver:str, token:str, sender:str = settings.email_sender):
    message = EmailMessage()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "Confirmation Email"

    with open(CONFIRM_EMAIL_TEMPLATE_PATH, encoding="utf-8") as file:
        html = file.read().replace("{{ link }}", create_confirm_link(token))
        message.set_content(html)
    message.add_alternative(html, subtype="html")
    
    ssl_context = ssl.create_default_context()

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls(context=ssl_context)
            smtp.ehlo()
            smtp.login(sender, settings.email_passcode)
            smtp.send_message(message)
    except SMTPException as e:
        raise HTTPException(
            status_code=500,
            detail="Не удалось отправить подтверждающее письмо. Попробуйте еще раз"
        )

def send_password_reset_email(receiver:str, token:str, sender:str = settings.email_sender):
    message = EmailMessage()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "Confirmation Email"

    with open(PASSWORD_RESET_EMAIL_TEMPLATE_PATH, encoding="utf-8") as file:
        html = file.read().replace("{{ reset_link }}", create_reset_link(token))
        message.set_content(html)
    message.add_alternative(html, subtype="html")
    
    ssl_context = ssl.create_default_context()

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls(context=ssl_context)
            smtp.ehlo()
            smtp.login(sender, settings.email_passcode)
            smtp.send_message(message)
    except SMTPException as e:
        raise HTTPException(
            status_code=500,
            detail="Не удалось отправить письмо для восстановления. Попробуйте еще раз"
        )


def create_confirm_link(token:str):
    return f"{settings.base_url}auth/confirm?token={token}"

def create_reset_link(token:str):
    return f"{settings.base_url}auth/password/reset/request?token={token}"
