from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import choice
import string
import smtplib

def send_mail(self, to):
    from os import environ
    from_u = 'trukeretruk@gmail.com'
    # passw = environ["EMAIL_PWD"]
    passw = 'Noquieroniloco!'

    msg = MIMEMultipart()
    msg['Subject'] = "Verificacion de cuenta de Trukere"
    msg['From'] = from_u
    msg['To'] = to

    body = "Hace click en este link para validar tu cuenta de Trukere " + \
           "http://127.0.0.1:8000/validate?email=" + to + "&code=" + \
           self.__verification_code

    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_u, passw)
    s.sendmail(from_u, to, text)
    s.close()