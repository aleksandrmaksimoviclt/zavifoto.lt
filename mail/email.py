from smtplib import SMTP_SSL
from email.mime.text import MIMEText

from django.conf import settings
from django.utils.safestring import mark_safe

from .models import EmailAutoReplySettings as Reply


class EmailSend(object):
    '''
    create EmailAutoReplySettings object
    call EmailSend object with below positional parameters in order,
    and call execute
    eg:
    auto_reply = EmailSend('Sashka', 'Labas', 'sashka@sashka.lt')
    auto_reply.execute()
    '''

    def __init__(self, name, client_message, client_email):
        _reply = Reply.objects.first()
        self.subject = _reply.subject
        self.message = _reply.text
        self.client_name = name
        self.client_message = client_message
        self.client_email = client_email

    def send(self, conn, send_to, subject, message):
        msg = MIMEText(message, 'html')
        msg['Subject'] = subject
        msg['From'] = '{} <{}>'.format('Zavifoto.lt', settings.EMAIL_HOST_USER)
        msg['To'] = send_to
        try:
            conn.send_message(msg)
        except Exception as e:
            print(e)
    
    def make_connection(self):
        try:
            conn = SMTP_SSL('{}:{}'.format(
                settings.EMAIL_HOST, settings.EMAIL_PORT))

            conn.login(
                settings.EMAIL_HOST_USER,
                settings.EMAIL_HOST_PASSWORD)
        except Exception:
            conn = False
        return conn

    def execute(self):
        connection = self.make_connection()
        if not connection:
            return 'SMTP Connection Failure'

        self.send(
            connection, self.client_email,
            self.subject, self.message)
        
        self.send(
          connection, 'aleksandr.maksimoviclt@gmail.com',
          'Nauja žinutė nuo {} ({})'.format(self.client_name, self.client_email),
          self.client_message)

        connection.quit()
        return 'Message sent'
