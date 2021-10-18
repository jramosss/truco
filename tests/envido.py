import sys
sys.path.append('../')
from api.classes.card import Card
from api.classes.deck import Deck
from api.classes.player import Player


d = Deck()
p = Player('jramos')

cards = d.get_cards(2)[0]

p.set_cards(cards)

p.print_mano()
print(p.points)
