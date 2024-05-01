from django.core.mail import send_mail
from django.utils.html import format_html

def send_report_email(link):
    email_to = "louisechristianboysillo@gmail.com"
    subject = 'MALICIOUS FOUND IN QR LINK REPORT!'
    modified_link = ' '.join(link)
    message = format_html(
        '<p>Greetings! </p>'
        '<p> This is SecQR reporting a malicious link:</p>'
        f'<p>{modified_link}</p>'
        '<p>Injected in a QR Code.</p>'
        '<p>Best regards,</p>'
        '<p>SecQR</p>'
    )
    from_email = 'secqr_app@outlook.com'
    send_mail(subject, message, from_email, [email_to], html_message=message)
    
