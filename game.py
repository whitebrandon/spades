from deck import Deck
from player import Player
from trick import Trick
from team import Team
from ai_characters import characters

from random import choice

class Game:
    
    def __init__(self, num_of_human_players, players=[]):
        self.deck = None
        self.num_of_human_players = num_of_human_players
        self.players = players
        self.active_player = None
        self.active_trick = None
        self.have_spades_been_broken = False
        self.teams = []
        self.round = 0

    def deal(self):
        """Deals cards to players and removes card from deck"""
        while self.deck.deck:
            for card, player in zip(self.deck.deck.copy(), self.players):
                player.get_card(card)
                card.set_owner(player)
                self.deck.deck.remove(card)

    def create_teams(self, num_of_teams, player_list):
        for _ in range(num_of_teams):
            self.teams.append(Team())
        self.assign_players_to_teams(num_of_teams, player_list)
        self.make_partnerships(self.teams)
        self.get_team_names(self.teams)

    def assign_players_to_teams(self, num_of_teams, player_list):
        for i in range(num_of_teams):
            for j in range(0,len(player_list), 2):
                self.teams[i].add_team_member(player_list[i+j])
                if j == 0:
                    self.teams[i].moderator = player_list[i+j]

    def make_partnerships(self, teams):
        for team in teams:
            for i in range(0, len(team), -1):
                team[i].partner = team[i-1]

    def get_team_names(self, teams):
        for team in teams:
            team.create_team_name()
            print(team.name) # delete this later

    def create_player(self, count):
        """Gets name of player from user, then creates Player"""
        name = input(f"Please enter a name for player {count + 1}: ")
        self.add_player(Player(name))

    def add_player(self, player):
        """Adds player to game"""
        self.players.append(player)

    def add_non_human_player(self, character_list):
        """Selects AI character from list and adds to game"""
        random_character = choice(character_list)
        character_list.remove(random_character)
        self.players.append(Player(random_character.fullname, True))

    def start_game(self):
        """Creates players for game and calls setup"""
        for i in range(self.num_of_human_players):
            self.create_player(i)
        for i in range(4 - (self.num_of_human_players)):
            self.add_non_human_player(characters)
        print("\n\n\n")
        self.create_teams(2, self.players)
        self.setup()

    def set_new_trick(self):
        """Resets trick"""
        self.active_trick = Trick()

    def add_trump_cards(self, card_list):
        """Adds trump cards to card list"""
        for card in self.active_trick.trick:
            if card.is_trump:
                card_list.append(card)

    def add_trick_suit_cards(self, card_list):
        """Adds cards with suits that match lead suit to card list"""
        for card in self.active_trick.trick:
            if card.suit == self.active_trick.suit:
                card_list.append(card)

    def sort_high_cards(self, card_list):
        """Sorts card list and returns in descending order"""
        return sorted(card_list, key = lambda x: x.value, reverse=True)

    def find_high_card(self):
        """Returns the highest card in the current trick"""
        highest_cards = []
        self.add_trump_cards(highest_cards)
        if not highest_cards:
            self.add_trick_suit_cards(highest_cards)
            return self.sort_high_cards(highest_cards)[0]
        else:
            return self.sort_high_cards(highest_cards)[0]

    def set_active_player(self):
        """Determines who the next active player should be"""
        current_players_index = self.players.index(self.active_player)
        next_players_index = current_players_index + 1
        self.active_player = self.players[next_players_index if current_players_index < len(self.players) - 1 else 0]

    def get_random_player(self, list_of_players):
        """Returns a random player from a list"""
        return choice(list_of_players)

    def is_round_over(self):
        """Checks if round is over"""
        for player in self.players:
            if player.hand:
                return False
        return True

    def evaluate_trick(self):
        """Finds and announces winner of trick, then returns winner"""
        winning_card = self.find_high_card()
        print("\n")
        print(f"The winning card is {winning_card}!")
        print("\n")
        return winning_card.owner

    def update_players_score(self, player):
        """Updates player's score and returns player"""
        player.score += 10
        return player

    def new_turn(self):
        """Initiates new turn"""
        if len(self.active_trick.trick) == len(self.players):
            self.active_player = self.update_players_score(self.evaluate_trick())
            if self.is_round_over():
                return # need to delete this later | just a way to keep game from going on forever
                # self.setup()
            else:
                return self.start_new_round()
        elif self.active_trick.trick:
            self.set_active_player()
        self.active_player = self.active_player or self.get_random_player(self.players)
        self.active_player.play_turn(self.active_trick, self.have_spades_been_broken)
        self.new_turn()

    def cleanup_players_hands(self):
        """Arranges hands of all players in game"""
        for player in self.players:
            player.arrange_hand()

    def start_new_round(self):
        """Starts new round of gameplay"""
        self.cleanup_players_hands()
        if self.round == 0:
            for player in self.players:
                if not player.is_computer:
                    print(player.hand)
        self.set_new_trick()
        self.collect_bids() if self.round == 0 else (0)
        self.round += 1
        self.new_turn()

    def setup(self):
        """Resets game"""
        self.show_scores_for_round() if self.round else print("The scores are all even at 0")
        # answer = input("Do you want to keep playing? [y/n]: ")
        # if answer.lower() == "n":
        #     return
        self.deck = Deck(True)
        self.deck.shuffle()
        self.deal()
        self.have_spades_been_broken = False
        self.start_new_round()   

    def show_scores_for_round(self):
        """Prints scores for all players"""
        for player in self.players:
            print(f"{player.name} has scored {player.score} points so far in the game!")

    def collect_bids(self):
        for player in self.players:
            if not player.is_computer:
                player.team.total_bid += player.bid_trick()
            else:
                player.team.total_bid += choice([1, 2, 3, 4, 5])
        self.announce_bid()

    def announce_bid(self):
        for team in self.teams:
            print(f"{team.name} bids {team.total_bid} for this round!")
