class Team:

    def __init__(self):
        self.score = 0
        self.name = None
        self.members = []
        self.captain = None
        self.total_bid = 0

    def add_team_member(self, player):
        self.members.append(player)
        player.team = self

    def create_team_name(self):
        self.name = "Team " + " & ".join([player.first for player in self.members])

    def __len__(self):
        return len(self.members)