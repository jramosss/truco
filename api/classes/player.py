from typing import List, Tuple
from typing_extensions import IntVar
from .card import Card

class Player:
    def __init__(self,user : str) -> None:
        self.user : str = user
        self.cards : List[Card] = []
        self.points : int = 0

    INVALID_CARDS = [Card(10,0),Card(10,1),Card(10,2),Card(10,3),
                    Card(11,0),Card(11,1),Card(11,2),Card(11,3),
                    Card(12,0),Card(12,1),Card(12,2),Card(12,3)]

    def get_user(self):
        return self.user
    
    def get_cards (self):
        return self.cards
    
    def set_cards (self,cards : List[Card]):
        self.cards = cards
        self.points = self.calc_points()
    
    def __calc_points_aux (self,card1 : Card,card2 : Card):
        
        points = 0
        print(f'__calc_points_aux: {card1.__str__()} , {card2.__str__()} , {card1 in self.INVALID_CARDS} , {card2 in self.INVALID_CARDS}')
        if card1 in self.INVALID_CARDS and card2 in self.INVALID_CARDS:
            points = 20
        elif card1 in self.INVALID_CARDS:
            points = 20 + card2.get_number()
        elif card2 in self.INVALID_CARDS:
            points = 20 + card1.get_number()
        else:
            points = 20 + card1.get_number() + card2.get_number()
        
        return points

    #def __calc_max_points (self):
        
    def __extract_data(self,card : Card):
        palo = card.palo
        value = card.number

        if (value >= 10):
            value = 0
    
        return palo, value


    def calc_points(self):
        cards = self.cards
        palo1, val1 = self.__extract_data(cards[0])
        palo2, val2 = self.__extract_data(cards[1])
        palo3, val3 = self.__extract_data(cards[2])

        if ((palo1 == palo2) and (palo2 == palo3)):
            
            points = 20 + val1+val2+val3
            
            if points > 33:
                auxMax = max([val1,val2,val3])
                auxMin = min([val1,val2,val3])
                
                if ((val1 > auxMin) and (val1 < auxMax)): points = 20 + val1 + auxMax
                if ((val2 > auxMin) and (val2 < auxMax)): points = 20 + val2 + auxMax
                if ((val3 > auxMin) and (val3 < auxMax)): points = 20 + val3 + auxMax
            
        elif ((palo1 == palo2) and (palo2 != palo3)):
            points = 20 + val1 + val2
        elif ((palo1 == palo3) and (palo1 != palo2)):
            points = 20 + val1 + val3
        elif ((palo2 == palo3) and (palo1 != palo2)):
            points = 20 + val2 + val3
        else:
            #print("Mentiste. No tenias nada para el envido")
            points = max([val1,val2,val3])
        
        return points

    #!Debug
    def print_mano (self):
        for card in self.cards:
            print(card.__str__())
    