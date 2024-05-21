from flask_mail import Message
from flask import current_app
from src.app import mail


def send_verification_email(to_email, verification_code):
    msg = Message('Código de verificación',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to_email])
    msg.body = f'Tu código de verificación es: {verification_code}'
    with current_app.app_context():
        mail.send(msg)


def verify_email_code(provided_code, stored_code):
    return provided_code == stored_code
