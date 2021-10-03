from api.utils.auth import get_username_from_token, valid_credentials
from db.models.user import check_email_status
from api.classes.room import Room, Rules
from db.models.db import load
from api.classes.room_hub import RoomHub
from db.models.room import RoomCreationRequest, get_rooms, remove_room_from_database, save_room_on_database
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_utils.tasks import repeat_every
from datetime import datetime, timedelta
from pprint import pprint


router = APIRouter()
hub = RoomHub()

@router.on_event("startup")
def load_hub():
    prev_rooms = load()
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
            await remove_room_from_database(room)


@ router.get('/rooms', tags=["Rooms"],status_code=200)
async def dump_rooms ():
    rooms = get_rooms()
    return {"rooms" : rooms}


@router.post("/room/new", tags=["Room"], status_code=status.HTTP_201_CREATED)
async def create_room(
        room_info: RoomCreationRequest,
        email: str = Depends(valid_credentials),
        username: str = Depends(get_username_from_token)):

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
        pprint(new_room.json())
        await save_room_on_database(new_room)
        hub.add_room(new_room)
        return {"message": "Room created successfully"}