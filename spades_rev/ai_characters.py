class AI:
    """Defines the creation of AI characters for card games"""
    def __init__(self, first, last, style=None):
        self.first_name = first
        self.last_name = last
        self.fullname = f"{self.first_name} {self.last_name}"
        self.style = style

    def __repr__(self):
        return f"AI({self.first_name}, {self.last_name})"

    def __str__(self):
        return self.fullname


sam_spade, robbie_heart, nell_diamond, tonya_clubb = [AI("Sam", "Spade", "aggressive"), AI("Robbie", "Hart"), AI("Nell", "Diamond"), AI("Tonya", "Clubb")]
characters = [sam_spade, robbie_heart, nell_diamond, tonya_clubb]