from game_state import GameState


class GameObject:
    """
    Parent class for all game objects: field and cell
    Stores information about game state
    """
    def __init__(self, game_state=None):
        self.game_state = game_state or GameState()
