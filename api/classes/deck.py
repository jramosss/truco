from random import shuffle
from typing import List
from card import Card

ALL_CARDS = [
        Card(1, 3),
        Card(1, 1),
        Card(7, 3),
        Card(7, 2),
        Card(3, 0),
        Card(3, 1),
        Card(3, 2),
        Card(3, 3),
        Card(2, 0),
        Card(2, 1),
        Card(2, 2),
        Card(2, 0),
        Card(1, 0),
        Card(1, 2),
        Card(12, 0),
        Card(12, 1),
        Card(12, 2),
        Card(12, 3),
        Card(11, 0),
        Card(11, 1),
        Card(11, 2),
        Card(11, 3),
        Card(10, 0),
        Card(10, 1),
        Card(10, 2),
        Card(10, 3),
        Card(7, 0),
        Card(7, 1),
        Card(6, 0),
        Card(6, 1),
        Card(6, 2),
        Card(6, 3),
        Card(5, 0),
        Card(5, 1),
        Card(5, 2),
        Card(5, 3),
        Card(4, 0),
        Card(4, 1),
        Card(4, 2),
        Card(4, 3),
]

class Deck:
    def __init__(self):
        self.used = []
        self.deck = ALL_CARDS
        shuffle(self.deck)


    def get_cards (self,n : int) -> List[List[Card]]:
        manos = []
        for _ in range (n):
            self.__print_mano(list(self.deck[0:3]))
            self.used.append(self.deck[0])
            self.used.append(self.deck[1])
            self.used.append(self.deck[2])
            self.deck.remove(self.deck[0])
            self.deck.remove(self.deck[1])
            self.deck.remove(self.deck[2])
        
        return manos


    def paraguaya (self,mano : List[Card]) -> List[Card]:
        new = self.deck[0:2]
        for card in mano:
            self.deck.append(card)
            self.used.remove(card)
        
        return new


    def shuffle(self):
        self.deck = ALL_CARDS
        shuffle(self.deck)
        self.used.clear()

    def __str__(self) -> str:
        strArr = []
        for card in self.deck:
            strArr.append(card.toString())
        
        return strArr


'''
if __name__ == '__main__':
    d = Deck()
    print("6 Players")
    d.print_card_list(d.get_cards(6))
    d.shuffle()
    print("4 Players")
    d.print_card_list(d.get_cards(4))
    d.shuffle()
    print("2 Players")
    d.print_card_list(d.get_cards(2))
'''
