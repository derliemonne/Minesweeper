import pygame as pg
from game_state import GameState
from field import Field
from additional_screen import AdditionalScreen
import sys


class GameEngine:
    """
    This class stores, draws and updates game objects
    """
    def __init__(self):
        self._SCREEN_SIZE = (500, 500)
        field_size = (500, 400)
        additional_field_size = (500, 100)
        self._FPS = 60
        self._screen = pg.display.set_mode(self._SCREEN_SIZE)
        self._clock = pg.time.Clock()
        self._game_state = GameState()
        self._field = Field(field_size, offset=(0, 100), game_state=self._game_state)
        self._additional_screen = AdditionalScreen(additional_field_size, self._game_state)
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
        dt = self._clock.tick(self._FPS)
        self._game_state.update(dt)
        pg.display.update()

    def draw(self):
        self._screen.blit(self._field.get_draw(), (0, 100))
        self._screen.blit(self._additional_screen.get_draw(), (0, 0))

    @staticmethod
    def exit():
        pg.quit()
        sys.exit()
