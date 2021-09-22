from fastapi import APIRouter
from db.models.user import User
from db.utils.check import check_username

router = APIRouter()

@ router.post('/login',tags=["Users"],status_code=200)
async def login (u : User):
    #if check_username(u) and 
    pass