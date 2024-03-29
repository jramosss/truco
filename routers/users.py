import bcrypt
from fastapi import APIRouter
from models.database_models import DBUser, db
from models.fastapi_models import User
from models.request_models import LoginRequest

router = APIRouter(prefix="/users")


@router.post('/register', tags=["Users"])
def register(user: User):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    if DBUser.select().where(DBUser.username == user.username).exists():
        return {"status": 400, "message": "Username already taken"}
    user = DBUser.create(username=user.username, password=hashed_password, email=user.email)
    return {'status': 201, 'message': 'User created'}


@router.post('/login', tags=["Users"])
def login(request: LoginRequest):
    user = DBUser.select().where(DBUser.username == request.identifier)
    if not user.exists():
        user = DBUser.select().where(DBUser.email == request.identifier)
    if not user.exists():
        return {'error': 'User not found', 'status': 404}
    else:
        user = list(user.execute())[0]
    if bcrypt.checkpw(request.password.encode('utf-8'), user.password.encode('utf-8')):
        return {'user': user, 'status': 200}
    else:
        return {'error': 'Wrong password', 'status': 401}


@router.get('/users', tags=["Debug"])
def get_users():
    users = DBUser.select()
    return {'users': list(users.execute(db)), 'status': 200}
