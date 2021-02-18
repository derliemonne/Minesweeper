import pygame as pg
from game_object import GameObject
from game_state import GameState
from minesweeper import sprites


class AdditionalScreen(GameObject):
    def __init__(self, surface_size: tuple, game_state: GameState):
        GameObject.__init__(self, game_state)
        self._surface = pg.Surface(surface_size)
        self._font = pg.font.SysFont('Arial', 30)

    def get_draw(self) -> pg.Surface:
        self._surface.fill(pg.color.Color('gray'))

        # render mines counter
        counter = self.game_state.mines_count - self.game_state.flags_count
        pos = (10, 20)
        self.draw_text(counter, pos)

        # render timer
        time_sec = self.game_state.time_ms / 1000
        pos = (380, 20)
        self.draw_text(time_sec, pos)

        return self._surface

    def draw_text(self, text, pos):
        self._surface.blit(
            self._font.render(str(text), True, pg.color.Color('black')),
            pos
        )
