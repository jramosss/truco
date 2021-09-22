from pony.orm.core import commit
from db.utils.utils import erase
from pydantic.networks import EmailStr
from api.utils.validator import Validation
from db.models.db import db
from db.utils.check import check_email2, check_username, check_email, check_validation_code
from db.utils.dumps import get_users
from fastapi import APIRouter, HTTPException
from db.models.user import User
from pony.orm import db_session
from api.utils.auth import hash_password
from datetime import datetime

router = APIRouter()


@router.post("/users/register", tags=["Users"], status_code=201)
async def register(user: User):
    """
    User register endpoint
    Params: User data->
      * username : str
      * email : EmailStr
      * password : str
    """
    if not check_username(user) and not check_email(user):
        with db_session:
            db.DB_User(
                username=user.username,
                email=user.email,
                hashed_password=hash_password(user.password),
                email_confirmed=False,
                icon=user.icon,
                creation_date=datetime.today().strftime("%Y-%m-%d"),
            )

        v = Validation()
        v.send_mail(user.email)
        # background_t.add_task(validator.send_mail, user.email)

        return {
            "message": user.username
            + ", a verification email has"
            + " been sent to "
            + user.email
        }
    else:
        msg = ""
        if check_username(user):
            msg += "Username already registered "
            raise HTTPException(
                status_code=409, detail="Username already registered ")
        elif check_email(user):
            msg += "Email already registered"
            raise HTTPException(
                status_code=409, detail="Email already registered")
        return {msg}


@router.get('/registered',tags=["Debug"],status_code=200)
async def dump_registered_users ():
    return {"Users: " : get_users()}


@router.get('/validate',tags=["Users"],status_code=200)
async def validate (email : EmailStr, code : str):
    if not check_email2(email):
        raise HTTPException(
            status_code=400, detail="Email not registered"
        )
    if check_validation_code(email,code):
        with db_session:
            user = db.DB_User.get(email=email)
            user.set(email_confirmed=True)
            commit()
        return {"Validated!"}
    else:
        raise HTTPException(
            status_code=404, detail="Invalid Code" 
        )


@router.get('/erase',tags=["Debug"],status_code=200)
async def erase_db (code : str):
    if code == '1574':
        erase()
        return {"Erased!"}
    else:
        raise HTTPException(
            status_code=403, detail="Invalid Code"
        )
