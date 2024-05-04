from email.message import EmailMessage
import ssl
import smtplib
import dramatiq

@dramatiq.actor
def send_email(total_price):
    email_sender = 'bunnylollabunny@gmail.com'
    email_password = 'wsnx prly vzgn megy'
    email_reciever = 'livaleria25@gmail.com'

    subject = 'Process your purchase from Adorine'
    body = f"""
    Thank You for your purchase! 
    Your final price for all items will be {total_price}.
    Come back to shop with us!
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciever
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())
