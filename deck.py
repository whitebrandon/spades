from card import Card, Joker
import random

class Deck:
    ranks = [
                ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), 
                ("7", 7), ("8", 8), ("9", 9), ("10", 10), 
                ("Jack", 11), ("Queen", 12), ("King", 13), ("Ace", 14)
            ]
    suits = ["♠ Spades ♠", "♥ Hearts ♥", "♣ Clubs ♣", "♦ Diamonds ♦"]
    jokers = [("Little", 15), ("Big", 16)]

    def __init__(self, jokers=False):
        self.deck = self.create_deck() #[]
        # self.create_deck()
        # if jokers:
        #     self.mix_in_jokers(Card("2","♥ Hearts ♥", 2), Card("2","♦ Diamonds ♦", 2))

    def create_deck(self):
        """Prepares a deck of 52 cards, no jokers"""
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(suit=suit, rank=rank[0], value=rank[1]))
        for joker in self.jokers:
            self.deck.append(Joker(size=joker[0], value=joker[1]))

    def shuffle(self):
        """Shuffles deck in place"""
        random.shuffle(self.deck)

    # def mix_in_jokers(self, card1, card2):
    #     """Substitutes jokers in for two other cards in deck"""
    #     self.deck = [card for card in self.deck if card != card1 and card != card2]
    #     for size in self.jokers:
    #         self.deck.append(Joker(size[0], size[1]))
    