import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
from model import EMAILSENT
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import create_engine
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_table(data, title,link):
    table_html = f"""
    <p><h2>{title}</h2><a href={link}>Site Link</a></p>
    <table border="1" cellpadding="5" cellspacing="0">
        <thead>
            <tr>
                <th>Title</th>
                <th>Date</th>
                <th>Link</th>
            </tr>
        </thead>
        <tbody>
    """
    for row in data:
        table_html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
        </tr>
        """
    
    table_html += """
        </tbody>
    </table>
    """  # Move the closing table tag and tbody tag here
    return table_html


def mailu(listu):
    load_dotenv()
    
    circulars=[]
    noti=[]
    for i in listu:
        if i[-1]=="circulars":
            circulars.append(i)
        else:
            noti.append(i)
    circtable=''
    notitable=''
    if len(circulars)!=0:
        circtable=generate_table(circulars,"Circulars","https://incometaxindia.gov.in/Pages/communications/circulars.aspx")
    if len(noti)!=0:
        notitable=generate_table(noti,"Notifications","https://incometaxindia.gov.in/Pages/communications/notifications.aspx")


    print(circtable)
    print(notitable)
    
    body='''
        <html>
    <body>
        <p>Hello,</p>
        <p>Here is the list of updated titles from the Income Tax India site.</p>
        <p>The following titles have been updated:</p>
        {circtableu}
        <br>
        {notitableu}    
        <p>Regards,<br>SIV</p>
    </body>
    </html>
'''.format(circtableu=circtable,notitableu=notitable)
    


    subject= "!!INCOME TAX UPDATE!! INCOMETAXINDIA has updated their site"


    print(body)
    email_sender=os.getenv("EMAIL_SENDER")
    email_password=os.getenv("EMAIL_PASSWORD")
    email_receivers=os.getenv("EMAIL_RECEIVER").split(",")
    print(email_receivers)



    em = EmailMessage()
    em['From']=email_sender
    em['To'] = ', '.join(email_receivers) 
    em['Subject']=subject
    em.set_content(body, subtype='html')
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
        print(f"email sent to {email_receivers}")
    
    DATABASE_URL = 'sqlite:///example.db'
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session=Session()
    email_reciever_string=",".join(email_receivers)
    email=EMAILSENT(sentto=email_reciever_string,senttime=datetime.now())
    session.add(email)
    session.commit()
    print("email sent to db")
    session.close()
        