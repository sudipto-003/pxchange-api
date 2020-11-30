from django.core.mail import EmailMessage
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()



class Util:
    @staticmethod
    def send_verification_mail(data):
        email = EmailMessage(subject=data['subject'], body=data['email_body'], to=[data['email_to']])
        EmailThread(email).start()