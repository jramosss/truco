from pony.orm import db_session, select
from db.models.db import  db


@db_session
def get_users ():
    return db.select('* from DB_User')