from random import shuffle
from typing import List, Tuple

class GameTeam:
    def __init__(self, players : List[str],points : int = 0) -> None:
        self.points = points
        self.players = players

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
    def __init__(self,players : List[str],max_points : int,
             rules, random_teams : bool = False,
              teams : tuple((List[str],List[str])) = ([],[])) -> None:
        self.players = players
        self.max_points = max_points
        self.rules = rules
        self.teams = gather_players(players) if random_teams else (GameTeam(teams[0]),GameTeam(teams[1]))

    def json (self):
        return {
            "players" : self.players,
            "rules" : self.rules.json(),
            "teams" : str(self.teams[0].toJSON()) + ' ' + str(self.teams[1].toJSON()),
            "max_points" : self.max_points
        }