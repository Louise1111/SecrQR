
import random
from django.core.mail import send_mail
from django.utils.html import format_html
def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

def send_otp_email(email, otp):
    subject = 'Forgot Password OTP'
    message = format_html(
        '<p>Greetings!</p>'
         '<p>Kindly input OTP to reset password.</p>'
         
        f'<p> OTP : {otp}</p>'
       
        '<p>Best regards,</p>'
        '<p>SecQR</p>'
    )
    from_email = 'secqr_app@outlook.com'  
    send_mail(subject, message, from_email, [email])