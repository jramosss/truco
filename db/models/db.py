from typing import List
from api.classes.room import Room, RoomStatus
from pony.orm import *
from datetime import date, datetime
from pydantic.networks import EmailStr

db = Database()

def define (**db_params):
    global db
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
        creation_date = Required(Json)

    class DB_Room(db.Entity):
        """
        Entity for the database, where we keep the status of the room
        and the game_state if begun.
        """

        name = PrimaryKey(str)
        max_players = Required(int)
        min_players = Required(int)
        current_players = Required(Json)
        owner = Required(str)
        status = Required(str)
        game = Required(Json)
        teams = Required(Json)
        created = Required(date)
        rules = Required(Json)


    class Validation_Tuple(db.Entity):
        """
        Database table used in storing the validation codes
        corresponding to each email registered.
        """

        email = PrimaryKey(EmailStr)
        code = Required(str)

    db.bind(**db_params)
    db.generate_mapping(create_tables=True)


def save():
    pass


def remove_room():
    pass
    