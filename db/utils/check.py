from re import U
from pony.orm import db_session
from pydantic.networks import EmailStr
from db.models.db import DB_Room, DB_User, db
from db.models.user import User

class UsernameNotFound (Exception):
    def __init__(self) -> None:
        self.message = "Username Not Found"

class IncorrectPassword (Exception):
    def __init__(self) -> None:
        self.message = "Incorrect Password"

@db_session
def check_username (u : User):
    uname = u.username
    return db.exists('SELECT * FROM DB_User u WHERE u.username = $uname')

@db_session
def check_email (u : User):
    email = u.email
    return db.exists('SELECT * FROM DB_User u WHERE u.email=$email')

@db_session
def check_email2 (email :EmailStr):
    return db.exists('SELECT * FROM DB_User u WHERE u.email=$email')

@db_session
def check_validation_code (email : EmailStr,code : str):
    return db.exists('SELECT * FROM Validation_Tuple v WHERE v.email=$email AND v.code=$code')
    
@db_session
def check_credentials (username : str,password : str):
    #TODO let the user enter the email or the username
    user = db.select('select * from DB_User where username=$username')
    try:
        if user[0][2] != password:
            raise IncorrectPassword()
    except IndexError:
        raise UsernameNotFound()

    return user[0]