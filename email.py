import smtplib
import os

server = smtplib.SMTP('smtp.gmail.com', 587)

email_sender=os.environ.get("EMAIL_SENDER")
email_password=os.environ.get("EMAIL_PASSWORD")
email_receiver=os.environ.get("EMAIL_RECEIVER")

server.start()
server.login("sktriple")