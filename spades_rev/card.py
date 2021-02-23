from playing_card_images import images

class Card:
    """Card to hold rank, suit and value"""

    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value
        self.owner = None
        self.playable = False
        self.is_trump = True if self.suit == "♠ Spades ♠" else False
        self.name = f'{self.rank} of {self.suit}'

    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"

    def __str__(self):
        return f"{images[self.name]} ({self.rank} of {self.suit})"

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit and self.value == other.value

    def __gt__(self, other):
        if self.is_trump and not other.is_trump:
            return True
        elif not self.is_trump and other.is_trump:
            return False
        elif self.is_trump and other.is_trump:
            return self.value > other.value
        return self.value > other.value

    def __lt__(self, other):
        if self.is_trump and not other.is_trump:
            return False
        elif not self.is_trump and other.is_trump:
            return True
        elif self.is_trump and other.is_trump:
            return self.value < other.value
        return self.value < other.value

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
        self.name = f'{self.rank} {self.suit}'


    def __repr__(self):
        return f"Joker({self.rank})"

    def __str__(self):
        return f"{images[self.name]}({self.rank} Joker)"