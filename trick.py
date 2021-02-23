class Trick:

    def __init__(self):
        self.suit = None
        self.trick = []

    def add_card_to_trick(self, card):
        """Adds a card to the trick"""
        self.trick.append(card)