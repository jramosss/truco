from enum import Enum
from inspect import Attribute
from random import randint
from datetime import datetime
from typing import List

from api.classes.game import Game

class Mano(Enum):
    EQUIPO = "Equipo"
    JUGADOR = "Jugador"

class Rules:
    def __init__(self, flor : bool, mano : str) -> None:
        self.flor = flor
        self.mano = mano

    def json (self):
        return {
            "flor" : self.flor,
            "mano" : self.mano
        }
    
    def fromJSON (self,json : object):
        return Rules(json['flor'],json['mano'])


class RoomStatus(Enum):
    LOBBY = "Lobby"
    INGAME = "In Game"
    FINISHED = "Finished"

default_rules = Rules(False,Mano.EQUIPO.value)
class Room:
    def __init__(self,name,owner : str,rules : Rules = default_rules,
                status : str = RoomStatus.LOBBY.value,
                min_players = 2,max_players = 6, max_points = 30,
                current_players : List[str] = []) -> None:
                #Remove this
        self.name = name
        self.min_players = min_players
        self.max_players = max_players
        self.current_players = current_players
        self.rules = rules
        self.owner = owner
        self.status = status
        self.messages = []
        self.teams = {"1" : [],"2" : []}
        self.created = datetime.now()
        self.max_points = max_points
        self.game = None


    def is_joinable (self):
        return len(self.current_players) < self.max_players and self.status == RoomStatus.LOBBY.value

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

    def get_owner(self) -> str:
        return self.owner

    def get_users (self):
        return self.current_players

    def get_status(self):
        return self.status

    def get_max_players(self):
        return self.max_players

    def set_status(self, status: str):
        self.status = status

    def set_rules (self,rules : Rules):
        self.rules = rules

    def set_teams (self,teams : object):
        self.teams = teams

    def set_created (self,created : datetime):
        self.created = created
    
    def set_max_points (self,max_points : int):
        self.max_points = max_points

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

    def json (self):
        return {
            "name" : self.name,
            "max_players" : self.max_players,
            "min_players" : self.min_players,
            "current_players" : self.current_players,
            "rules" : self.rules.json(),
            "max_points" : self.max_points,
            "teams" : self.teams,
            "status" : self.status,
            "created" : self.created,
            "owner" : self.owner
        }
    
    def start_game (self,random_teams : bool = False,teams = ([],[])):
        self.set_status(RoomStatus.INGAME.value)
        self.game = Game(self.current_players,self.max_points,self.rules,random_teams,teams)


