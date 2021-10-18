from random import choice, shuffle
from typing import List, Tuple
from player import Player
from deck import Deck

class GameTeam:
    def __init__(self, players : List[Player],points : int = 0) -> None:
        self.points = points
        self.players = players
        self.pie : Player = None # calc

    def toJSON (self):
        return {
            "points" : self.points,
            "players" : self.players
        }
    
    def fromJSON (self,json : object):
        return GameTeam(json['players'],json['points'])


#Generate random teams
def gather_players (players : List[str]):
    n = len(players)
    shuffle(players)
    team1 = [players[i] for i in range(n//2)]
    team2 = [players[i] for i in range(n//2,n)]

    return (GameTeam(team1),GameTeam(team2))

class Game:
    def __init__(self,users : List[str],max_points : int,
             rules, random_teams : bool = False,
              teams : tuple((List[str],List[str])) = ([],[])) -> None:
        self.players = self.init_players(users)
        self.max_points = max_points
        self.rules = rules
        self.teams = gather_players(self.players) if random_teams else (GameTeam(teams[0]),GameTeam(teams[1]))
        self.deck : Deck = Deck()
        self.mano : GameTeam = choice(self.teams)

    def json (self):
        return {
            "players" : self.players,
            "rules" : self.rules.json(),
            "teams" : str(self.teams[0].toJSON()) + ' ' + str(self.teams[1].toJSON()),
            "max_points" : self.max_points
        }

    def init_players (self,users: List[str]):
        players : List[Player] = []
        for user in users:
            players.append(Player(user))
        
        return players

    def distribute_cards (self):
        manos = self.deck.get_cards(len(self.players))
        for player,mano in self.players,manos:
            player.set_cards(mano)