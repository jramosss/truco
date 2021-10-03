from pony.orm import db_session
from fastapi import HTTPException,status,Depends
from db.models.db import db
from api.utils.auth import verify_password,valid_credentials
from db.utils.check import IncorrectPassword, UsernameNotFound


@db_session
#TODO let the user login with username or email
#TODO let the user login using third party
def authenticate_user(mail: str, password: str):
    """
    Function that autenthicates the user by checking his password
    """
    keys = ('username', 'email', 'hashed_password',
            'email_confirmed', 'icon', 'creation_date')
    try:
        user_tuple = db.get("select * from DB_User where email = $mail")
        if not user_tuple:
            raise UsernameNotFound
    except:
        raise HTTPException(
            status_code=400, detail="Incorrect mail address")
    user = dict(zip(keys, user_tuple))
    if not verify_password(password, user['hashed_password']):
        raise IncorrectPassword
    return user



async def get_current_user(email: str = Depends(valid_credentials)):
    """
    Function that return a dict with all the users data from the database
    """
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    keys = ('username', 'email', 'hashed_password',
            'email_confirmed', 'icon', 'creation_date')
    with db_session:
        try:
            user_tuple = db.get(
                "select * from DB_User where email = $email")
        except:
            raise HTTPException(
                status_code=400, detail="Incorrect email or password")
        user = dict(zip(keys, user_tuple))
    return user