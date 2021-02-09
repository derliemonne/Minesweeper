from game_state import GameState
from game_object import GameObject
from minesweeper import sprites


class Cell(GameObject):
    """
    Stores information about cell
    There are methods to change cell state
    """
    def __init__(self, game_state: GameState):
        GameObject.__init__(self, game_state)
        self.is_opened = False
        self.is_mined = False
        self.is_flagged = False
        self.mined_neighbors_count = 0

        _sheet = sprites.TileSheets(sprites.TileSheets.two_thousand)
        _builder = sprites.TileBuilder(_sheet)
        self._tile = _builder.build()

    def open(self):
        self.is_opened = True

    def change_flag(self):
        self.is_flagged = not self.is_flagged

    def get_sprite(self):
        """
        :return: sprite that can be blitted on a surface
        """
        if not self.is_opened:
            return self._tile.flag if self.is_flagged else self._tile.unopened
        else:
            if self.is_mined:
                if self.game_state.is_game_win:
                    return self._tile.mine_red_cross
                return self._tile.mine_red if self.game_state.is_game_over else self._tile.mine
            else:
                return self._tile[str(self.mined_neighbors_count)]  # a digit 0-8


