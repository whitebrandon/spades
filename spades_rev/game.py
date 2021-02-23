import random
import copy
from time import sleep

from player import Player
from ai_characters import characters
from team import Team
from deck import Deck
from trick import Trick

class Game:

    def __init__(self):
        self.players = None
        self.deck = None
        self.teams = None
        self.current_lead = None
        self.victory_score = None

    def start_game(self):
        # Announce start of game
        print("\n♠♠♠♠♠♠ Let's play Spades! ♠♠♠♠♠♠\n")
        self.players = self.get_players()
        self.teams = self.choose_teams(self.players)
        self.deck, self.current_lead = self.draw_for_lead(self.players)
        print(f"{self.current_lead} drew the high card and will lead off first.")
        self.victory_score = self.determine_endgame_score()
        self.deck = self.shuffle(self.deck)
        self.deal(self.deck, self.players)
        print("\nThe teams are:\n\n♠♡♣♢ {} ♠♡♣♢\n\n♠♡♣♢ {} ♠♡♣♢.\n".format(*[team.name for team in self.teams.values()]))
        self.teams = self.collect_bids(self.teams)
        self.play_round(self.players, self.teams, self.victory_score)

    def get_players(self):
        """Finds out amount of sentient players,
           creates the players, and adds them to list
        """
        human_player_count = 0
        print("How many people will be playing?")
        while not human_player_count:
            try:
                # Ask how many humans are playing
                human_player_count = int(input("Enter a number between (1 and 4): "))
                if human_player_count < 1 or human_player_count > 4:
                    human_player_count = 0
                    raise ValueError("The number of people playing can't be less than 1 or more than 4. Please try again.", 1)
            except ValueError as err:
                msg = "Oh no! Something's not right."
                if not len(err.args) > 1:
                    print(msg, "The value you entered does not seem to be a number. Please try again.")
                else:
                    print(msg, err.args[0])
        # Create an instance of a player object for each human player
        players = []
        for i in range(human_player_count):
            first_name, *other_names = input(f"Please enter a name for Player {i + 1}. ").split(" ")
            last_name = ""
            if other_names and len(other_names) > 1:
                *middle_name, last_name = other_names
                first_name = " ".join([first_name, *middle_name])
            else:
                last_name = other_names[0]
            players.append(Player([first_name.strip(), last_name.strip()]))
        # Create an instance of a player object for each a.i.
        for i in range(4 - human_player_count):
            ai = random.choice(characters)
            characters.remove(ai)
            players.append(Player(ai, True))
        # Add all players to a list
        return players

    def choose_teams(self, players):
        # Determine the amount of teams
        num_teams = int(input("How many teams are players being split into? ")) or len(players)
        teams = {}
        # Create a team object for each team
        for i in range(num_teams):
            teams[i+1] = Team()
        # Add the appropriate players to appropriate team object
            for j in range(0,len(players), 2):
                teams[i+1].add_team_member(players[i+j])
                players[i+j].partner = players[i+j-2]
                if j == 0:
                    teams[i+1].captain = players[i+j]
        # Create team name for each team
        for team in teams.values():
            team.create_team_name()
        return teams

    def draw_for_lead(self, player_list):
        print("Let's draw cards to see which player leads off.")
        players = copy.deepcopy(player_list)
        # Create deck
        deck = Deck()
        # remove low twos
        for card in deck.deck:
            if str(card) in ["2 of ♡ Hearts ♡", "2 of ♣ Clubs ♣"]:
                deck.deck.remove(card)
            elif str(card) == "2 of ♠ Spades ♠":
                card.value = 15
        # Shuffle deck
        deck = self.shuffle(deck)
        # Have each player draw a card
        for player in players:
            player.hand = deck.draw()
            player.hand.owner = player
            print(f'{player.first} drew the {player.hand}!')
            sleep(1.0)
        # Determine high card
        high_card = sorted([player.hand for player in players])[-1]
        # Set winner of high card to be lead
        return (deck, list(filter(lambda player: player == high_card.owner, player_list))[0])
    
    def determine_endgame_score(self):
        victory_score = 0
        print("A typical game of Spades has a goal of 500 points, but any goal of 200 points or more works.")
        # Determine the total points needed for victory
        while not victory_score:
            try:
                victory_score = int(input("What point total would you like to signal victory? "))
                if victory_score < 200:
                    victory_score = 0
                    raise ValueError("If the Victory Score is less than 200, the game ends up being too short. Please try again.", 1)
                elif victory_score > 2000:
                    victory_score = 0
                    raise ValueError("That Victory Score is a bit high for a game of Spades. Please try a number between 200 and 2000.", 1)
            except ValueError as err:
                msg = "Oh no! Something's not right."
                if not len(err.args) > 1:
                    print(msg, "The value you entered does not seem to be a number. Please try again.")
                else:
                    print(err.args[0])
        # Announce the total to the players
        print(f"It's time to get things rolling. First team to {victory_score} points, wins the game!")
        return victory_score

    def shuffle(self, deck):
        deck = copy.deepcopy(deck)
        # Shuffle order of cards in deck
        random.shuffle(deck.deck)
        # Return new deck
        return deck

    def deal(self, deck, player_list):
        """Deals cards to players and removes card from deck"""
        deck = copy.deepcopy(deck.deck)
        while deck:
            for card, player in zip(deck.copy(), player_list):
                player.get_card(card)
                card.set_owner(player)
                deck.remove(card)
        return None

    def collect_bids(self, teams_dict):
        teams_dict = copy.deepcopy(teams_dict)
        teams = copy.deepcopy(teams_dict)
        players = [player for team in teams.values() for player in team.members]
        tricks_per_round = int(len(self.deck.deck)/len(players))
        processing_initial_bids = True
        # Ask players for their bids
        while processing_initial_bids:
            for player in list(filter(lambda player: not player.is_computer, players)):
                player.arrange_hand()
                print(f"{player.first} this is your hand: ", ", ".join(str(card) for card in player.hand))
                bid_guess = 0
                while not bid_guess:
                    try:
                        bid_guess = int(input("How many tricks will you win? "))
                        if bid_guess < 1 or bid_guess > tricks_per_round:
                            bid_guess = 0
                            raise ValueError("Sorry. There are no Nil bids or bids for more than the total tricks per round.", 1)
                    except ValueError as err:
                        msg = "Oh no! Something's not right."
                        if not len(err.args) > 1:
                            print(msg, "The value you entered does not seem to be a number. Please try again.")
                        else:
                            print(err.args[0])
                    else:
                        player.guess = bid_guess
            processing_initial_bids = False
        for player in list(filter(lambda player: player.is_computer, players)):
            high_cards = []
            for card in player.hand:
                if card.value >= 13:
                    high_cards.append(card)
            player.guess = len(high_cards) or 1
        for team in teams.values():
            bid_list = []
            official_bid = 0
            for member in team.members:
                bid_list.append(member.guess)
            # total bid can't be lt 4 or highest bid b/w members (i.e. if a player bids 6, their team can't bid lt that)
            bid_list.sort(reverse=True)
            low = bid_list[0] if bid_list[0] > 4 else 4
            if not team.captain.is_computer:
                print(f"{team.captain.first}, now is the time for you to lock in your team's official bid.")
                print(f"It can be as low as {low} tricks or as high as {tricks_per_round} tricks.")
                print(f"Your team's current UNOFFICIAL bid is {4 if sum(bid_list) < 4 else sum(bid_list)} tricks.", end=" ")
                print(f"(Your partner, {team.captain.partner.first} thinks they can win {team.captain.partner.guess} trick", "s.)" if team.captain.partner.guess > 1 else ".)", sep="")
                response = input(f"Would you like to lock in {4 if sum(bid_list) < 4 else sum(bid_list)} tricks as your OFFICIAL bid? [y/N] ")
                if response.lower() in ["n", "no"]:
                    while not official_bid:
                        try:
                            official_bid = int(input(f"{team.captain.first}, enter your team's official bid. [{low}-{tricks_per_round}] "))
                            if official_bid < low or official_bid > tricks_per_round:
                                official_bid = 0
                                raise ValueError(f"Sorry. Your team's bid can't be lower than {low} tricks or higher than {tricks_per_round} tricks.", 1)
                        except ValueError as err:
                            msg = "Oh no! Something's not right."
                            if not len(err.args) > 1:
                                print(msg, "The value you entered does not seem to be a number. Please try again.")
                            else:
                                print(err.args[0])
            # Add partners bids together
                else: 
                    official_bid = 4 if sum(bid_list) < 4 else sum(bid_list)
            else:
                # given the way the computer bids, the most their sum of guesses would be is 10 (all k's/q's and both jkrs)
                official_bid = 4 if sum(bid_list) < 4 else sum(bid_list)
            # Announce Team bids
            print(f"{team.name} bids {official_bid} tricks for this round.")
            team.total_bid = official_bid
        for key, value in teams_dict.items():
            for k, v in teams.items():
                if key == k:
                    value.total_bid = v.total_bid
        return teams_dict


    def play_round(self, player_list, teams, victory_score):
        # A trick count is initalized to zero
        trick_count = 0
        spades = {"is_broken": False}
        player_list = player_list
        while trick_count < 13:
            trick_count += 1
            trick = Trick()
            find_high_card = self.find_high_card
            # Lead player leads off trick
            # reorder players so that lead player has index of 0
            index_of_lead = player_list.index(self.current_lead)
            lead_order = player_list[index_of_lead:]
            lead_order.extend(player_list[:index_of_lead])
            # Players play cards in turn
            # When all players have played a card
            # The winning card is determined
            for player in lead_order:
                find_high_card = find_high_card(player.play_turn(trick, spades))
                sleep(1.0)
            print()
            # The winning player takes the trick
            print(f"The winner of that round is {find_high_card.owner.fullname} with a winning card of {find_high_card}")
            find_high_card.owner.tricks.append(trick)
            # The winning player is set as the lead player
            self.current_lead = find_high_card.owner
        # The scores are updated
        self.update_scores(player_list, teams)
        # The scores are checked to see if a team has won
        # The round is reset 
        self.reset_play()

    def find_high_card(self, lead_card):
        trick = [lead_card]
        high_card = lead_card
        def check_higher(card):
            """Sets lead of trick as high card
            then waits until all cards are in before returning winning card"""
            trick.append(card)
            nonlocal high_card
            high_card = (card if (card.is_trump and not high_card.is_trump) or
                        (card.is_trump and card.value > high_card.value) or
                        (card.value > high_card.value and card.suit == high_card.suit) else high_card)
            return high_card if len(trick) == len(self.players) else check_higher
        return check_higher

    def update_scores(self, players, teams):
        # Add each team's score for the round to running total 
        for team in teams.values():
                tricks_won = len([trick for member in team.members for player in players if player.fullname == member.fullname for trick in player.tricks])
                # for player in players:
                #     for member in team.members:
                #         if player.fullname == member.fullname:
                #             member = player
                if tricks_won >= team.total_bid:
                    team.score += (team.total_bid * 10) + (tricks_won - team.total_bid) 
                    print(f"{team.name} | Score: {team.score}")
                else:
                    team.score -= team.total_bid * 10
                    print(f"{team.name} | Score: {team.score}")

    def reset_play(self):
        # Shuffle deck
        self.deck = self.shuffle(self.deck)
        # Deal cards
        self.deal(self.deck, self.players)
        # Collect bids
        self.teams = self.collect_bids(self.teams)
        # Play the next round
        self.play_round(self.players, self.teams, self.victory_score)

    def quit_game(self):
        # Announce end of game
        # Return
        pass
