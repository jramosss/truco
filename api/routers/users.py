from pony.orm.core import commit
from db.utils.login import authenticate_user, get_current_user
from db.utils.utils import erase
from pydantic.networks import EmailStr
from api.utils.validator import Validation
from db.models.db import db
from db.utils.check import check_email2, check_username, check_email, check_validation_code
from db.utils.dumps import get_users
from fastapi import APIRouter, HTTPException, status, Depends
from db.models.user import User, Token, check_email_status
from pony.orm import db_session
from api.utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, valid_credentials, get_logged_users
from datetime import datetime
from api.utils.auth import create_access_token
from datetime import timedelta
from db.utils.check import IncorrectPassword, UsernameNotFound
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

#!Debug
me = User(username='Chuls',password='Heladera65',email='jramostod@gmail.com')

@router.post("/register", tags=["Users"], status_code=201)
async def register(user: User = me):
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
                hashed_password=get_password_hash(user.password),
                email_confirmed=False,
                icon=user.icon,
                creation_date=datetime.today().strftime("%Y-%m-%d"),
            )
            commit()

        if user == me:
            with db_session:
                user = db.DB_User.get(email=user.email)
                user.set(email_confirmed=True)
                commit()
            return {"Listo mostroo"}
        else:
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


@router.get('/registered+',tags=["Debug"],status_code=200)
async def dump_registered_users_premium():
    me = get_users()[0]
    email_confirmed = check_email_status(me[1])
    return {f"Me: {me} {email_confirmed}"}


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


@router.post("/users", tags=["Users"], response_model=Token, status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    LogIn endpoint, first, authenticates the user checking that the
    email and the password submitted by the user are correct.
    Then it creates a valid token for the user.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user["email"], "username": user["username"]},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@ router.post('/token',tags=["Users"],status_code=200)
async def login (form : OAuth2PasswordRequestForm = Depends()):
    try:
        user = authenticate_user(form.username,form.password)
    except UsernameNotFound:
        return {"Username not found"}
    except IncorrectPassword:
        return {"Incorrect Password"}

    ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    access_token = create_access_token(
        data={"email": user["email"], "username": user["username"]},
        expires_delta=ACCESS_TOKEN_EXPIRES,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/users/refresh", tags=["Login"], response_model=Token, status_code=201)
#async def refresh_token(email: str = Depends(valid_credentials)):
async def refresh_token(email : str = 'jramostod@gmail.com'):
    """
    Endpoint that creates a new web token.
    As the funciton "updates" creating a new token, it has the PUT method.
    Need to be logged in to use.
    """
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        with db_session:
            username: str = db.get(
                "select username from DB_User where email=$email")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"email": email, "username": username},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(
            status_code=405,
            detail="Something went wrong"
        )


@router.get('/logged',tags=["Debug"],status_code=200)
async def dump_logged_users  ():
    users = get_logged_users()
    return {"users" : users}


@router.get("/users/me", status_code=200, tags=["Users"])
async def read_users(current_user: User = Depends(get_current_user)):
    '''
    API endpoint that serves for testing the token validation. Returns info about
    the user that logged in if validation went well
    '''
    return (current_user)