import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl

load_dotenv()
def mailu():
    email_sender=os.getenv("EMAIL_SENDER")
    email_password=os.getenv("EMAIL_PASSWORD")
    email_receivers=os.getenv("EMAIL_RECEIVER").split(",")
    print(email_receivers)
    subject= "!IMPORTANT! INCOMETAXINDIA has updated their site"
    body='''
    hello,
    CHECK THE SITE NOW : https://incometaxindia.gov.in/Pages/communications/circulars.aspx
    regards,
    SIV
    '''

    em = EmailMessage()
    em['From']=email_sender
    em['To'] = ', '.join(email_receivers) 
    em['Subject']=subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
        print(f"email sent to {email_receivers}")