
import random
from django.core.mail import send_mail

def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

def send_otp_email(email, otp):
    subject = 'Forgot Password OTP'
    message = f'Your OTP for password reset is: {otp}'
    from_email = 'secqr_app@outlook.com'  # Replace with your email
    send_mail(subject, message, from_email, [email])