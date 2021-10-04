from fastapi.param_functions import Path
from api.utils.auth import get_username_from_token, valid_credentials
from db.models.user import check_email_status
from api.classes.room import Mano, Room, RoomStatus, Rules
from api.classes.room_hub import RoomHub
from db.models.room import RoomCreationRequest, get_rooms, load_from_database, remove_room_from_database, save_room_on_database
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_utils.tasks import repeat_every
from datetime import datetime, timedelta
from pprint import pprint
from db.models.db import db
from pony.orm import db_session


router = APIRouter()
hub = RoomHub()

room0 = Room(name='room0',owner='jramostod@gmail.com')
room1 = Room(name='room1',owner='jramostod@gmail.com',rules=Rules(True,Mano.EQUIPO.value))
room2 = Room(name='room2',owner='jramostod@gmail.com',rules=Rules(True,Mano.JUGADOR.value))
room3 = Room(name='room3',owner='jramostod@gmail.com',rules=Rules(False,Mano.JUGADOR.value))
room4 = Room(name='room4',owner='jramostod@gmail.com',rules=Rules(False,Mano.EQUIPO.value))

sample_rooms = [room0,room1,room2,room3,room4]

@router.on_event("startup")
def load_hub():
    prev_rooms = load_from_database()
    for room in prev_rooms:
        hub.add_room(room)


@router.on_event("startup")
@repeat_every(seconds=60, wait_first=True)
async def clean_hub_and_db():
    for room in hub.rooms:
        owner = room.get_owner()
        count = room.get_user_count()
        last_update_delta = datetime.now() - room.get_last_update()
        if ((owner is None and count <= 0)
                or (last_update_delta > timedelta(seconds=600))):
            hub.remove_room(room)
            remove_room_from_database(room)

@db_session
def sample_rooms_created () -> bool:
    created = 0
    for room in sample_rooms:
        r = db.DB_Room.get(name=room.name)
        if r:
            created += 1

    return created == len(sample_rooms)

#!DEBUGGING
@router.on_event('startup')
async def create_sample_rooms ():
    if sample_rooms_created():
        return
    
    for room in sample_rooms:
        save_room_on_database(room)
        hub.add_room(room)

    print("Sample rooms created")

@ router.get('/rooms', tags=["Room"],status_code=200)
async def dump_rooms ():
    rooms = get_rooms()
    return {"rooms" : rooms}


@router.post("/room/new", tags=["Room"], status_code=status.HTTP_201_CREATED)
async def create_room(
        room_info: RoomCreationRequest,
        email: str = Depends(valid_credentials)):

    """
    Endpoint for creating a new room.

    Possible responses:\n
            201 when succesfully created.
            401 when not logged in.
            403 when email not confirmed.
            409 when the room name is already in use.
            500 when there's an internal error in the database.
    """

    room_name = room_info.name
    min = room_info.min_players
    max = room_info.max_players
    r = Rules(room_info.flor,room_info.mano)
    email_confirmed = check_email_status(email)

    if not email_confirmed:
        raise HTTPException(status_code=403, detail="E-mail not confirmed")
    elif room_name in (hub.all_rooms()):
        raise HTTPException(status_code=409,
                            detail="Room name already in use")
    else:
        new_room = Room(name=room_name,min_players=min ,max_players=max, rules=r,owner=email)
        save_room_on_database(new_room)
        hub.add_room(new_room)
        return {"message": "Room created successfully"}


@ router.get("/room/join/{room_name}", tags=["Room"], status_code=status.HTTP_200_OK)
async def join_room(
        room_name: str = Path(
            ...,
            min_length=2,
            max_length=20,
            description="The name of the room you want to join",
        ),
        email: str = Depends(valid_credentials)):
    """
    Endpoint to join a room, it takes the room name as a parameter in the URL,
    and the access_token in the request headers.

    Possible responses:\n
            200 when succesfully joined.
            401 when not logged in.
            403 when email not confirmed or room is full.
            404 when the room doesn't exist.
            409 when the user is already in the room.
            403 when the room is full or in-game.
    """

    room = hub.get_room_by_name(room_name)
    if not check_email_status(email):
        raise HTTPException(status_code=403,
                            detail="E-mail is not confirmed")
    elif not room:
        raise HTTPException(status_code=404, detail="Room not found")
    elif email in room.current_players:
        return {"message": "User already in the room"}
    elif not room.is_joinable():
        if len(room.current_players) == room.max_players:
            raise HTTPException(status_code=403,
                            detail="Room is full")    
        else:
            raise HTTPException(status_code=403,
                            detail="Room is in-game")
    else:
        room.join(email)
        save_room_on_database(room)
        return {"message": f"Joined {room_name}"}


@ router.get("/room/leave/{room_name}", tags=["Room"], status_code=status.HTTP_200_OK)
async def leave_room(
        room_name: str = Path(
            ...,
            min_length=2,
            max_length=20,
            description="The name of the room you want to leave",
        ),
        email: str = Depends(valid_credentials)):
    """
    Endpoint to leave a room, it takes the room name as a parameter in the URL,
    and the access_token in the request headers.

    Possible respones:\n
            200 when succesfully left.
            401 when not logged in.
            403 when email not confirmed.
            404 when the room doesn't exist.
            409 when the user is not in the room.
            403 when the room is full or in-game.
    """

    room = hub.get_room_by_name(room_name)
    if not check_email_status(email):
        raise HTTPException(status_code=403,
                            detail="E-mail is not confirmed")
    elif not room:
        raise HTTPException(status_code=404, detail="Room not found")
    elif email not in room.get_users():
        raise HTTPException(status_code=409,
                            detail="You're not in this room")
    elif room.status == RoomStatus.INGAME.value:
        raise HTTPException(status_code=403, detail="Room is in-game")
    else:
        room.leave(email)
        return {"message": f"Left {room_name}"}