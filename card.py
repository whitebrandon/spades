class Card:
    """Card to hold rank, suit and value"""

    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value
        self.owner = None
        self.playable = False
        self.is_trump = True if self.suit == "♠ Spades ♠" else False

    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __gt__(self, other):
        return self if self.value > other.value else other

    def __lt__(self, other):
        return self if self.value < other.value else other

    def set_owner(self, player):
        """Sets a player to be the owner of the card"""
        self.owner = player

class Joker(Card):

    def __init__(self, size, value):
        super().__init__(size, None, value)
        self.rank = size
        self.suit = "Joker"
        self.value = value
        self.is_trump = True


    def __repr__(self):
        return f"Joker({self.rank})"

    def __str__(self):
        return f"{self.rank} Joker"