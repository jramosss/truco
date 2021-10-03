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
        creation_date = Required(datetime)

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

@ db_session
def load():
    db_rooms = []
    try:
        with db_session:
            db_rooms = db.DB_Room.select()
    except Exception as e:
        print(e)

    rooms = []
    for room in db_rooms:
        new_room = Room(room.name, room.max_players, room.owner)
        new_room.current_players = room.current_players
        if room.status == RoomStatus.LOBBY.value:
            new_room.set_status(RoomStatus.LOBBY)
        elif room.status == RoomStatus.INGAME.value:
            new_room.set_status(RoomStatus.INGAME)
        else:
            new_room.set_status(RoomStatus.FINISHED)

        if (new_room.get_status() != RoomStatus.LOBBY and room.game is not {}):
            #new_room.game = Game(new_room.get_user_list())
            new_room.game.build_from_json(room.game)

        rooms.append(new_room)

    return rooms


def save():
    pass


def remove_room():
    pass
    