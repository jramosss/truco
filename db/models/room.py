from typing import Optional
from pony.orm.core import delete
from api.classes.room import Mano, Room
from pydantic import BaseModel, Field
from pony.orm import db_session
from db.models.db import db


class RoomCreationRequest(BaseModel):
    """
    Body of the request used to create a new room,
    Identifying owner by email isn't optimal(?)
    """

    name: str = Field(..., min_length=2, max_length=20, description="The room's name")
    min_players : int = Field(...,ge=2,le=6,description="Minimun players required in the room")
    max_players: int = Field(
        ..., ge=2, le=6, description="Max allowed players in the room"
    )
    flor : Optional[bool] = False
    mano : Optional[Mano] = Mano.EQUIPO


class ChatRequest(BaseModel):
    """
    Body of the request used for sending messages to the chat.
    """

    msg: str = Field(
        ..., max_length=256, min_length=1, description="The message you want to send"
    )


@db_session
def get_rooms ():
    return db.select('select * from DB_Room')

def save_room_on_database(room: Room):
    json = room.json()
    room_name = room.name
    try:
        with db_session:
            if (db.exists("select * from DB_Room where name = $room_name")):
                db_room = db.DB_Room.get(name=room_name)
                db_room.set(min_players=room.min_players)
                db_room.set(max_players=room.max_players)
                db_room.set(current_players={"users": room.get_users()})
                db_room.set(rules=room.rules.json())
                db_room.set(owner=room.get_owner())
                db_room.set(status=room.get_status())
                db_room.set(game={})
                db_room.set(teams=json["teams"])
                db_room.set(created=room.created)
            else:
                db.DB_Room(
                    name=room_name,
                    min_players=room.min_players,
                    max_players=room.get_max_players(),
                    current_players={"current_players": room.current_players},
                    owner=room.get_owner(),
                    status=room.get_status().value,
                    game={},
                    teams=json["teams"],
                    created=room.created,
                    rules=room.rules.json()
                )
    except Exception as e:
        print(f"Something went wrong on the db, {e}")


async def remove_room_from_database(room: Room):
    try:
        room_name = room.get_name()
        with db_session:
            delete(r for r in db.DB_Room if r.name == room_name)
    except Exception as e:
        print(e)