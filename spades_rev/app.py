"""Starts the game
"""
from game import Game

def app():
    """Creates a new game and calls start_game on it"""
    game = Game()
    game.start_game()


if __name__ == "__main__":
    app()
