class GameState:
    """
    Structure for storing and accessing game state
    """
    def __init__(self):
        self.is_game_over = False
        self.is_game_win = False
        # player has just started a game
        self.is_first_move = True

