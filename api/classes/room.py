from enum import Enum
from random import randint
from datetime import datetime
from typing import List

class Mano(Enum):
    EQUIPO = "Equipo"
    JUGADOR = "Jugador"

class Rules:
    def __init__(self, flor : bool, mano : Mano) -> None:
        self.flor = flor
        self.mano = mano


class RoomStatus(Enum):
    LOBBY = "Lobby"
    INGAME = "In Game"
    FINISHED = "Finished"


class Team:
    def __init__(self,members : List[str], points : int) -> None:
        self.members = members
        self.points = points


class Room:
    def __init__(self,name,status : RoomStatus,rules : Rules,min_players = 2,max_players = 6, max_points = 30) -> None:
        self.name = name
        self.min_players = min_players
        self.max_players = max_players
        self.current_players = []
        self.rules = rules
        self.owner = None
        self.status = status
        self.messages = []
        self.team1 = Team([],0)
        self.team2 = Team([],0)
        self.created = datetime.now().date().timetuple()
        self.max_points = max_points
        self.game = None


    def is_joinable (self):
        return len(self.current_players) < self.max_players and self.status == RoomStatus.LOBBY

    def join (self, email : str):
        if self.is_joinable():
            self.current_players.append(email)
        if self.owner is None:
            self.owner = email

    def leave (self,email : str):
        self.current_players.remove(email)
        if self.owner == email and self.current_players != []:
            self.owner = self.current_players[randint(0,len(self.current_players))]
        if self.current_players ==  []:
            # Remove room from db
            pass

    def get_game (self):
        return self.game

    def get_name(self):
        """ Room name getter"""
        return self.name

    def get_user_count(self):
        """User count getter"""
        return len(self.current_players)

    def get_owner(self):
        return self.owner

    def get_users (self):
        return self.current_players

    def get_status(self):
        return self.status

    def get_max_players(self):
        return self.max_players

    def set_status(self, status: RoomStatus):
        self.status = status

    def update_status(self):
        game = self.get_game()
        #phase = game.get_phase()
        #if (phase in [GamePhase.FO_WON, GamePhase.DE_WON]):
        #    self.set_status(RoomStatus.FINISHED)

    def dump_game_json(self):
        game = self.get_game()
        if self.get_game() is not None:
            pass
        else:
            json = {}
        return json

    def can_user_chat(self, username: str):
        in_room = username in self.current_players
        #socket_exists = username in self.sockets.keys()
        if self.get_game() is None:
            can_chat = True
        elif in_room:
            can_chat = self.get_game().player_can_speak(username)
        else:
            can_chat = False

        return (in_room and can_chat)

    def post_message(self, msg):
        self.messages.append(msg)
        if (len(self.messages) > 32):
            self.messages.pop(0)

    def get_messages(self):
        return self.messages

    