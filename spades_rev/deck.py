from card import Card, Joker

class Deck:
    ranks = [
                ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), 
                ("7", 7), ("8", 8), ("9", 9), ("10", 10), 
                ("Jack", 11), ("Queen", 12), ("King", 13), ("Ace", 14)
            ]
    suits = ["♠ Spades ♠", "♡ Hearts ♡", "♣ Clubs ♣", "♢ Diamonds ♢"]
    jokers = [("Little", 16), ("Big", 17)]

    def __init__(self):
        self.deck = self.create_deck()

    def __repr__(self) -> str:
        return str(self.deck)

    def create_deck(self):
        """Prepares a deck of 54 cards"""
        deck = [Card(suit=suit, rank=rank[0], value=rank[1]) for suit in self.suits for rank in self.ranks]
        for joker in self.jokers:
            deck.append(Joker(size=joker[0], value=joker[1]))
        return deck

    def draw(self):
        top_card = self.deck.pop()
        self.deck.insert(0, top_card)
        return top_card
