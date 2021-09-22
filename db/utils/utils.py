from db.models.db import DB_Room, DB_User, Validation_Tuple
from db.models.user import User
from pony.orm import db_session
from pony.orm.core import delete

def erase ():
  with db_session:
    delete(u for u in DB_User)
    delete(r for r in DB_Room)
    delete(vt for vt in Validation_Tuple)