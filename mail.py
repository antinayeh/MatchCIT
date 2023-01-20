from flask_mail import Mail, Message
from typing import List
from config import sender_email

import re

title = "Your Dating Matches are in!"

class Match:
    def __init__(self, name, email) -> None:
        self.name =  name
        self.email = email


    def __str__(self) -> str:
        return f"Name: {self.name}, Email: {self.email}"


def format_email(name: str, matches: List[Match]) -> str:
    return f'''Hi {name},

Your dating matches are in!
1: {matches[0]},
2: {matches[1]}, 
3: {matches[2]} 

Thank you!
'''


def send_email(app, mail_handler, recipient_email: str, content: str):
    if re.match("[0-9]+@gmail.com", recipient_email) is not None:
        app.logger.debug(f"skipping {recipient_email}")
        return f"skipping {recipient_email}"
    msg = Message(title, sender=sender_email, recipients = [recipient_email])
    app.logger.debug(f"Sending email {content} to {recipient_email}")
    msg.body = content
    mail_handler.send(msg)
    return f"Sent email {content} to {recipient_email}"

