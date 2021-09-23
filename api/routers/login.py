from db.utils.utils import user_row_to_dict
from api.utils.auth import create_access_token
from datetime import timedelta
from fastapi import APIRouter
from fastapi.params import Depends
from db.models.user import User
from db.utils.check import IncorrectPassword, UsernameNotFound, check_credentials
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@ router.post('/login',tags=["Users"],status_code=200)
async def login (form : OAuth2PasswordRequestForm = Depends()):
    try:
        user = check_credentials(form.username,form.password)
    except UsernameNotFound:
        return {"Username not found"}
    except IncorrectPassword:
        return {"Incorrect Password"}

    print(user)
    ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    user_dict = user_row_to_dict(user)
    access_token = create_access_token(
        data={"email": user_dict["email"], "username": user_dict["username"]},
        expires_delta=ACCESS_TOKEN_EXPIRES,
    )
    return {"access_token": access_token, "token_type": "bearer"}
