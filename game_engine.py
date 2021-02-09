import pygame as pg
from game_state import GameState
from field import Field
import sys


class GameEngine:
    """
    This class stores, draws and updates game objects
    """
    def __init__(self):
        self.screen_size = (500, 400)
        self.screen = pg.display.set_mode(self.screen_size)
        self.clock = pg.time.Clock()
        self.fps = 60
        self.game_state = GameState()
        self.field = Field(self.screen_size, game_state=self.game_state)
        self.mouse_event_handlers = []
        self.key_event_handlers = []

        self.key_event_handlers.append(self.handle_exit)
        self.mouse_event_handlers.append(self.field.handle_mouse_event)

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
                for handler in self.key_event_handlers:
                    handler(event.key)
            elif event.type == pg.MOUSEBUTTONDOWN:
                for handler in self.mouse_event_handlers:
                    handler(event.pos, event.button)

    def handle_exit(self, key):
        if key == pg.K_ESCAPE:
            self.exit()

    def update(self):
        # stable fps
        self.clock.tick(self.fps)
        pg.display.update()

    def draw(self):
        self.field.draw(self.screen)

    @staticmethod
    def exit(self):
        pg.quit()
        sys.exit()
