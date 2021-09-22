from pony.orm import *
from datetime import date
from pydantic.networks import EmailStr

db = Database()


class DB_User(db.Entity):
    """
    Entity for the database, the password is stored hashed, and
    the db uses the user email as PK
    """

    username = Required(str)
    email = PrimaryKey(str)
    hashed_password = Required(str)
    email_confirmed = Required(bool)
    icon = Optional(str)
    creation_date = Required(date)

class DB_Room(db.Entity):
    """
    Entity for the database, where we keep the status of the room
    and the game_state if begun.
    """

    name = PrimaryKey(str)
    max_players = Required(int)
    owner = Required(str)
    status = Required(str)
    users = Required(Json)
    emails = Required(Json)
    game = Required(Json)

class Validation_Tuple(db.Entity):
    """
    Database table used in storing the validation codes
    corresponding to each email registered.
    """

    email = PrimaryKey(EmailStr)
    code = Required(str)

db.bind(provider='sqlite', filename='db.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


def load():
    pass


def save():
    pass


def remove_room():
    pass
    