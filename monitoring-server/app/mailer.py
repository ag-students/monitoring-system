import smtplib, os
from dotenv import load_dotenv

load_dotenv()

gmail_user = 'vanekkravtsov85@gmail.com'
gmail_password = os.getenv('GMAIL_PASSWORD')

def send_mail(email_to):
    From = gmail_user
    subject = 'Attention!'
    body = 'Something go wrong! Go to home and check.'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (From, ', '.join(email_to), subject, body)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(From, email_to, email_text)
    server.close()
    print('Email sent!')
