from fastapi import APIRouter
from db.models.user import User
from db.utils.check import IncorrectPassword, UsernameNotFound, check_credentials

router = APIRouter()

@ router.post('/login',tags=["Users"],status_code=200)
async def login (u : User):
    try:
        user = check_credentials(u.username,u.password)
    except UsernameNotFound:
        return {"Username not found"}
    except IncorrectPassword:
        return {"Incorrect Password"}

    return {"Logged in"}
