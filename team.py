class Team:

    # teams need a name
    # teams need to keep track of their total books
    def __init__(self):
        self.total_tricks = 0
        self.name = None # should receive in instance creation?
        self.members = [] # should receive in instance creation?
        self.moderator = None
        self.total_bid = 0

    def add_team_member(self, player):
        self.members.append(player)
        player.team = self

    def create_team_name(self):
        player_names = map(lambda player: player.first , self.members)
        self.name = "Team " + " and ".join(player_names)

    def __len__(self):
        return len(self.members)