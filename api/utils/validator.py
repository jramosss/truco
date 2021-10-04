from db.models.db import db  # ,Validation_Tuple
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pony.orm import db_session, commit
import string
import smtplib
from secrets import choice , token_urlsafe
#from dotenv import load_dotenv

#load_dotenv('.env')

class Validation:
    #TODO make the validation mail expire after some time
    def __init__(self):
        self.__verification_code : str = self.__generate_random_string(8)

    def __generate_random_string(self, length):
        letters = string.ascii_uppercase + string.digits
        result_str = ''.join(choice(letters) for _ in range(length))
        return result_str

    @db_session
    def send_mail(self, to):
        from os import environ
        from_u = 'trukeretruk@gmail.com'
        #passw = environ["EMAIL_PWD"]
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

        db.Validation_Tuple(email=to, code=self.__verification_code)
        # For some reason i can not do this and get the same result
        commit()