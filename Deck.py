import random

# Uses 9 through Ace
# 4 players, each dealt 5, 4 left over in the kitty
# Each card has a number and a suit
#   Dictionary
# Four suits

#SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
SUITS = [0, 1, 2, 3]
#CARDS = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
CARDS = [0, 1, 2, 3, 4, 5]

class Deck:

    def __init__(self):
        self.deck = [0 for n in range(24)]
        n = 0
        for i in SUITS:
            for j in CARDS:
                self.deck[n] = {'suit' : i, 'number' : j}
                n += 1
        self.players = [0,0,0,0]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        self.players[0] = random.sample(self.deck, 5)
        reduced_deck = [card for card in self.deck if card not in self.players[0]]
        self.players[1] = random.sample(reduced_deck, 5)
        reduced_deck = [card for card in reduced_deck if card not in self.players[1]]
        self.players[2] = random.sample(reduced_deck, 5)
        reduced_deck = [card for card in reduced_deck if card not in self.players[2]]
        self.players[3] = random.sample(reduced_deck, 5)

# Demonstrates one round of dealing cards
# def main():
#     test = Deck()
#     print(test.deck, 'sorted')
#     print()
#     test.shuffle()
#     print(test.deck, 'shuffled')
#     print()
#     test.deal()
#     print(test.hand_1, '1')
#     print()
#     print(test.hand_2, '2')
#     print()
#     print(test.hand_3, '3')
#     print()
#     print(test.hand_4, '4')
#     print()
#     print(test.kitty, 'kitty')
#     print()

# main()
