from db.models.user import User
from pony.orm import db_session
from pony.orm.core import delete
from db.models.db import db

def erase ():
  with db_session:
    delete(u for u in db.DB_User)
    delete(r for r in db.DB_Room)
    delete(vt for vt in db.Validation_Tuple)
