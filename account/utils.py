import random
from django.core.mail import send_mail
from django.utils.html import format_html

def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

def send_otp_email(email, otp):
    subject = 'Forgot Password OTP'
    message = format_html(
        '<div style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; border-radius: 10px;">'
        '<h2 style="color: #333; text-align: center;">Forgot Password OTP</h2>'
        '<p style="text-align: center;">Hi!</p>'
        '<p style="text-align: center;">Please input OTP to reset your password:</p>'
        f'<p style="text-align: center; font-weight: bold;">OTP: {otp}</p>'

        '<p style="text-align: center; font-style: italic;">SecQR</p>'
        '<div style="text-align: center;">'
        '<img src="https://i.ibb.co/pyyWq9T/secqr-logo-secure.png" alt="SecQR Logo" style="width: 60px; height: 30px; margin-bottom: 20px;">'
        '</div>'
        '</div>'
    )
    from_email = 'secqr_app@outlook.com'
    send_mail(subject, message, from_email, [email], html_message=message)
