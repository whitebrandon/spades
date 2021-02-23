from ai_characters import AI
import random

class Player:
    
    def __init__(self, names: list, is_computer=False):
        self.first, self.last = names if not isinstance(names, AI) else [names.first_name, names.last_name]
        self.fullname = " ".join([self.first, self.last])
        self.hand = []
        self.team = None
        self.partner = None
        self.tricks = []
        self.is_computer = is_computer

    def __repr__(self):
        return f"Player({self.fullname})"

    def __str__(self):
        return self.fullname

    def __eq__(self, other: object) -> bool:
        return self.fullname == other.fullname

    def get_card(self, card):
        """Adds card to hand"""
        self.hand.append(card)

    def find_suits(self):
        """Finds unique suits in current hand and returns a list of them"""
        unique_suits = set()
        for card in self.hand:
            if not card.suit == "Joker":
                unique_suits.add(card.suit)
        return list(unique_suits)

    def group_suits(self, lst):
        """Groups cards of same suit together into multi dimension list and returns it"""
        grouped_suits = [[] for _ in range(len(lst))]
        for card in self.hand:
            card.suit = "♠ Spades ♠" if card.suit == "Joker" else card.suit
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


    def activate_hand(self, trick, spades):
        """Returns list of cards in player's hand that can be played"""
        self.toggle_cards(self.hand, False)
        if trick.suit is not None:
            return self.get_normal_options(trick)
        else:
            return self.get_lead_options(spades)

    def select_card(self, trick, spades):
        """Returns player's card selection"""
        cards_in_play = self.activate_hand(trick, spades)
        selection = cards_in_play[self.print_options(cards_in_play)]
        if selection.is_trump:
            spades['is_broken'] = True
        return selection

    def play_turn(self, trick, spades):
        """Selects and plays a card"""
        selected_card = self.select_card(trick, spades)
        trick.add_card_to_trick(selected_card)
        self.hand.remove(selected_card)
        print(f"{self.first} played the {str(selected_card)}")
        # print("\n")
        trick.suit = selected_card.suit if trick.suit is None else trick.suit
        return selected_card

    def get_normal_options(self, trick):
        """Returns all cards that player can play"""
        cards_in_play = list(filter(lambda card: (card.suit == trick.suit or
                                                 (trick.suit == "♠ Spades ♠" and card.suit == "Joker") or 
                                                 (trick.suit == "Joker" and card.suit == "♠ Spades ♠")), 
                                                 self.hand))
        if not cards_in_play: # if you can't follow suit
            return self.toggle_cards(self.hand)
        else:
            return self.toggle_cards(cards_in_play)

    def get_lead_options(self, spades):
        """Returns all cards that player can lead with"""
        if spades['is_broken']:
            return self.toggle_cards(self.hand)
        else:
            cards_in_play = list(filter(lambda card: card.suit != "♠ Spades ♠" and card.suit != "Joker", self.hand))
            if not cards_in_play:
                spades['is_broken'] = True
                return self.toggle_cards(self.hand)
            else:
                return self.toggle_cards(cards_in_play)

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
            selection = int(input(f"Which card would you like to play, {self.first}? ")) - 1
            print("\n")
        else:
            selection = random.randint(0, len(card_list) - 1)
        return selection
