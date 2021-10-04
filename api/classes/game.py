from random import shuffle
from typing import List, Tuple
from room import Mano, Rules

class GameTeam:
    def __init__(self,points : int, players : List[str]) -> None:
        self.points = points
        self.players = players


#Generate random teams
def gather_players (players : List[str]):
    n = len(players)
    shuffle(players)
    team1 = [players[i] for i in range(n//2)]
    team2 = [players[i] for i in range(n//2,n)]

    return (GameTeam(0,team1),GameTeam(0,team2))
    




class Game:
    def __init__(self,players : List[str],max_points : int,
             rules : Rules, random_teams : bool = False,
              teams : Tuple(List[str],List[str]) = ([],[])) -> None:
        self.players = []
        self.max_points = max_points
        self.rules = rules
        self.teams : Tuple(List[str],List[str]) = gather_players(players) if random_teams else teams




if __name__ == '__main__':
    g = Game(['1','2','3','4','5','6'],30,Rules(True,Mano.EQUIPO))