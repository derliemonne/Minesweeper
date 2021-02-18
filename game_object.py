from game_state import GameState
import pygame as pg


class GameObject:
    """
    Parent class for all game objects: field and cell
    Stores information about game state
    """
    def __init__(self, game_state=None):
        self.game_state = game_state or GameState()

    def get_draw(self) -> pg.Surface:
        pass
