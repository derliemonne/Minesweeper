class GameState:
    """
    Structure for storing and accessing game state
    """
    def __init__(self):
        self.is_game_over = False
        self.is_game_win = False
        # player has just started a game
        self.is_first_move = True
        self.mines_count = 10
        self.flags_count = 0
        self.time_ms = 0

    def update(self, dt):
        # if game has started
        if not self.is_first_move and not self.is_game_over and not self.is_game_win:
            self.time_ms += dt
