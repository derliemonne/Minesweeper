import pygame as pg
from game_state import GameState
from field import Field
import sys


class GameEngine:
    """
    This class stores, draws and updates game objects
    """
    def __init__(self):
        self._SCREEN_SIZE = (500, 400)
        self._FPS = 60
        self._screen = pg.display.set_mode(self._SCREEN_SIZE)
        self._clock = pg.time.Clock()
        self._game_state = GameState()
        self._field = Field(self._SCREEN_SIZE, game_state=self._game_state)
        self._mouse_event_handlers = []
        self._key_event_handlers = []

        self._key_event_handlers.append(self.handle_exit)
        self._mouse_event_handlers.append(self._field.handle_mouse_event)

    def run(self):
        while 'ok':
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit()
            elif event.type == pg.KEYDOWN:
                for handler in self._key_event_handlers:
                    handler(event.key)
            elif event.type == pg.MOUSEBUTTONDOWN:
                for handler in self._mouse_event_handlers:
                    handler(event.pos, event.button)

    def handle_exit(self, key):
        if key == pg.K_ESCAPE:
            self.exit()

    def update(self):
        # stable fps
        self._clock.tick(self._FPS)
        pg.display.update()

    def draw(self):
        self._field.draw(self._screen)

    @staticmethod
    def exit():
        pg.quit()
        sys.exit()
