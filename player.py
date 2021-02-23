import random

class Player:
    
    def __init__(self, name, is_computer=False):
        self.name = name
        self.first, self.last = name.split(" ")
        self.hand = []
        self.team = None
        self.partner = None
        self.score = 0
        self.is_computer = is_computer

    def __repr__(self):
        return f"Player({self.name})"

    def __str__(self):
        return self.name

    def __add__(self, other):
        return self.name + other.name

    def get_card(self, card):
        """Adds card to hand"""
        self.hand.append(card)

    def find_suits(self):
        """Finds unique suits in current hand and returns a list of them"""
        unique_suits = set()
        for card in self.hand:
            unique_suits.add(card.suit)
        return list(unique_suits)

    def group_suits(self, lst):
        """Groups cards of same suit together into multi dimension list and returns it"""
        grouped_suits = [[] for _ in range(len(lst))]
        for card in self.hand:
            index = lst.index(card.suit)
            grouped_suits[index].append(card)
        return grouped_suits

    def sort_suits(self, nested_lst):
        """Sorts items in a nested list in descending order"""
        rearranged_hand = []
        for suit in nested_lst:
            suit.sort(key= lambda card: card.value, reverse=True)
            for card in suit:
                rearranged_hand.append(card)
        return rearranged_hand

    def arrange_hand(self):
        """Rearranges current hand by suit"""
        unique_suits = self.find_suits()
        grouped_suits = self.group_suits(unique_suits)
        self.hand = self.sort_suits(grouped_suits)

    def bid_trick(self):
        """Returns int of amount of tricks player thinks they can win"""
        bid_guess = int(input("How many tricks will you win? "))
        return bid_guess

    def activate_hand(self, trick, spades_in_play):
        """Returns list of cards in player's hand that can be played"""
        self.toggle_cards(self.hand, False)
        if trick.suit is not None:
            return self.get_normal_options(trick)
        else:
            return self.get_lead_options(spades_in_play)

    def select_card(self, trick, spades_in_play):
        """Returns player's card selection"""
        cards_in_play = self.activate_hand(trick, spades_in_play)
        return cards_in_play[self.print_options(cards_in_play)]

    def play_turn(self, trick, spades_in_play):
        """Selects and plays a card"""
        selected_card = self.select_card(trick, spades_in_play)
        trick.add_card_to_trick(selected_card)
        self.hand.remove(selected_card)
        print(f"{self.name} played the {str(selected_card)}")
        print("\n")
        if trick.suit is None:
            trick.suit = selected_card.suit

    def get_normal_options(self, trick):
        """Returns all cards that player can play"""
        trick.suit = "♠ Spades ♠" if trick.suit == "Joker" else trick.suit
        cards_in_play = list(filter(lambda card: card.suit == trick.suit, self.hand))
        if trick.suit == "♠ Spades ♠":
            self.check_and_add_jokers(cards_in_play)
        if not cards_in_play:
            return self.toggle_cards(self.hand)
        else:
            return self.toggle_cards(cards_in_play)

    def get_lead_options(self, spades_in_play):
        """Returns all cards that player can lead with"""
        if spades_in_play:
            return self.toggle_cards(self.hand)
        else:
            cards_in_play = list(filter(lambda card: card.suit != "♠ Spades ♠" and card.suit != "Joker", self.hand))
            if not cards_in_play:
                return self.break_spades(spades_in_play)
            else:
                return self.toggle_cards(cards_in_play)

    def break_spades(self, spades_in_play):
        """Allows for spades to be led on following trick"""
        spades_in_play = True
        return self.toggle_cards(self.hand)

    def toggle_cards(self, card_list, boolean=True):
        """Sets the playability of a list of cards, then returns it"""
        for card in card_list:
            card.playable = boolean
        return card_list

    def print_options(self, card_list):
        """Prints the options of cards the player can choose, then returns choice"""
        selection = None
        if not self.is_computer:
            for index, card in enumerate(card_list):
                print(f'Enter {index + 1} to play the {str(card)}')
            print("\n")
            selection = int(input(f"Which card would you like to play, {self.name}? ")) - 1
            print("\n")
        else:
            selection = random.randint(0, len(card_list) - 1)
        return selection

    def check_and_add_jokers(self, card_list):
        """Checks for jokers in hand, and (if any) adds them to card list""" 
        for card in self.hand:
            if card.suit == "Joker":
                card_list.append(card)