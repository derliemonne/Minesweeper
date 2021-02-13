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
        self._is_opened = False
        self._is_mined = False
        self._is_flagged = False
        self._mined_neighbors_count = 0

        _sheet = sprites.TileSheets(sprites.TileSheets.two_thousand)
        _builder = sprites.TileBuilder(_sheet)
        self._tile = _builder.build()

    @property
    def is_opened(self):
        return self._is_opened

    def open(self):
        self._is_opened = True

    @property
    def is_mined(self):
        return self._is_mined

    @is_mined.setter
    def is_mined(self, value: bool):
        self._is_mined = value

    @property
    def is_flagged(self):
        return self._is_flagged

    @property
    def mined_neighbors_count(self):
        return self._mined_neighbors_count

    @mined_neighbors_count.setter
    def mined_neighbors_count(self, value):
        self._mined_neighbors_count = value

    def change_flag(self):
        self._is_flagged = not self._is_flagged

    def get_sprite(self):
        """
        :return: sprite that can be blit on a surface
        """
        if self._is_opened:
            if self._is_mined:
                return self._tile.mine_red_cross if self.game_state.is_game_win else self._tile.mine_red
            else:
                return self._tile[self._mined_neighbors_count]  # a digit 0-8
        else:
            return self._tile.flag if self._is_flagged else self._tile.unopened
