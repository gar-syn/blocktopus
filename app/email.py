from threading import Thread
from flask_mail import Message
from . import mail
from flask import render_template
from flask import current_app
import app
    
def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    print(user.email)
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
