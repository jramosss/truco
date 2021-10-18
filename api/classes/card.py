from enum import Enum
from random import Random, random

class Palo(Enum):
    BASTO = 1
    ORO = 2
    ESPADA = 3
    COPA = 4

    def from_int (palo : int) -> str:
        if palo == 0:
            return 'copa'
        elif palo == 1:
            return 'basto'
        elif palo == 2:
            return 'oro'
        elif palo == 3:
            return 'espada'
        else:
            return f'invalid number {palo}'

'''
0 - Copa
1 - Basto
2 - Oro
3 - Espada
'''
class Card:
    def __init__(self, number: int, palo: int):
        self.number = number if number != -1 else Random().randint(1,12)
        self.palo = palo if palo != -1 else Random().randint(0,3)

    def get_number(self):
        return self.number

    def get_palo(self):
        return self.palo

    def get_hierarchy(self):
        hierarchy = {
            Card(1, 3): 14,
            Card(1, 1): 13,
            Card(7, 3): 12,
            Card(7, 2): 11,
            Card(3, 0): 10,
            Card(3, 1): 10,
            Card(3, 2): 10,
            Card(3, 3): 10,
            Card(2, 0): 9,
            Card(2, 1): 9,
            Card(2, 2): 9,
            Card(2, 0): 9,
            Card(1, 0): 8,
            Card(1, 2): 8,
            Card(12, 0): 7,
            Card(12, 1): 7,
            Card(12, 2): 7,
            Card(12, 3): 7,
            Card(11, 0): 6,
            Card(11, 1): 6,
            Card(11, 2): 6,
            Card(11, 3): 6,
            Card(10, 0): 5,
            Card(10, 1): 5,
            Card(10, 2): 5,
            Card(10, 3): 5,
            Card(7, 0): 4,
            Card(7, 1): 4,
            Card(6, 0): 3,
            Card(6, 1): 3,
            Card(6, 2): 3,
            Card(6, 3): 3,
            Card(5, 0): 2,
            Card(5, 1): 2,
            Card(5, 2): 2,
            Card(5, 3): 2,
            Card(4, 0): 1,
            Card(4, 1): 1,
            Card(4, 2): 1,
            Card(4, 3): 1,
        }   
        return hierarchy[Card(self.number, self.palo)]

    def __str__(self) -> str:
        return str(self.number) + " de " + str(Palo.from_int(self.palo))

    def __eq__(self, o: object) -> bool:
        return self.number == o.number and self.palo == o.palo