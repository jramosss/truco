from pydantic import BaseModel, Field
from typing import Optional
from pydantic.networks import EmailStr
from db.models.db import db
from pony.orm import db_session

class User(BaseModel):
    """
    BaseModel for the user, in which we collect the necessary data
    to be able to save the user in the database
    It does not include the password, so it comes separately and is hashed
    once received.
    """

    username: str = Field(..., min_length=4, max_length=20)
    email: EmailStr
    password: str = Field(
        ...,
        min_length=6,
        max_length=54,
        regex="^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,32}$",
    )
    icon: str = 'string'
    email_confirmed: Optional[bool] = False


class Token(BaseModel):
    """
    Model for tokens, it contains the token_type and the string
    of the token
    """

    access_token: str
    token_type: str


class NewPassword(BaseModel):
    old_pwd: str
    new_pwd: str = Field(
        ...,
        min_length=6,
        max_length=54,
        regex="^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,32}$",
    )


class NewUsername(BaseModel):
    username: str = Field(..., min_length=4, max_length=20)

@ db_session
def check_email_status (email : str) -> bool:
    user = db.DB_User.get(email=email)
    return user.email_confirmed