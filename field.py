from game_object import GameObject
from game_state import GameState
import pygame as pg
from pygame import Vector2 as Vector
from cell import Cell
import numpy as np
from random import randint


class Field(GameObject):
    """
    It holds cells
    Updates and draws them depending on game state and events (mouseclick)
    """
    def __init__(self, screen_size: tuple, game_state: GameState):
        GameObject.__init__(self, game_state)
        self.field_size = (10, 8)
        width, height = self.field_size
        self.cells = np.array([[Cell(game_state=self.game_state)
                               for _y in range(height)]
                               for _x in range(width)])
        self.mines_count = 10
        self.cell_size = min([screen_size[i] // self.field_size[i] for i in range(2)])
        self._mine_vectors = None

    def generate(self, clicked_cell_vector):
        """
        Player has no chance to blow up on mine in the very beginning
        Therefore the field is being generating after the first click
        The first cell the player clicks must have zero mined neighbors
        :param clicked_cell_vector: coordinates of the cell player clicked
        :return:
        """
        width, height = self.field_size
        self._mine_vectors = []
        # 1) generating random coordinates to place mine
        while len(self._mine_vectors) < self.mines_count:
            random_vector = (randint(0, width - 1), randint(0, height - 1))
            if (random_vector not in self._mine_vectors and
                    random_vector != clicked_cell_vector and
                    random_vector not in self.get_neighbor_vectors(clicked_cell_vector)):
                self._mine_vectors.append(random_vector)
        # 2) setting mines
        for vector in self._mine_vectors:
            self.cells[vector].is_mined = True
            for coordinates in self.get_neighbor_vectors(vector):
                self.cells[coordinates].mined_neighbors_count += 1

    def get_neighbor_vectors(self, vector):
        """
        :param vector: coordinates of cell whose neighbors to count
        :return: a list of (x, y) coordinates of neighbors
        """
        neighbors_vectors = []
        width, height = self.field_size
        x, y = tuple(vector)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                # there is no reason to count itself
                if dx == dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < width and 0 <= new_y < height:
                    neighbors_vectors.append((new_x, new_y))
        return neighbors_vectors

    def expose_cell(self, vector):
        """
        Handles opening the cell when player clicks on it
        :param vector: coordinates of cell player clicked
        :return:
        """
        # already opened cells can't be changed
        if self.cells[vector].is_opened:
            return
        if self.cells[vector].is_mined:
            self.blow_up()
            return
        # on the first move the field had not been generated yet
        if self.game_state.is_first_move:
            self.generate(vector)
            self.game_state.is_first_move = False

        self.cells[vector].open()
        if self.cells[vector].mined_neighbors_count == 0:
            for neighbor_vector in self.get_neighbor_vectors(vector):
                # recursive exposing
                self.expose_cell(neighbor_vector)
        # player could have just opened the last cell that is not mined
        self.check_game_win()

    def check_game_win(self):
        opened_cells_count = len([1 for row in self.cells for cell in row if cell.is_opened])
        left_cells_count = (self.field_size[0] * self.field_size[1]) - opened_cells_count
        if left_cells_count == self.mines_count:
            self.game_state.is_game_win = True
            for vector in self._mine_vectors:
                # just open mined cells to show player the win
                self.cells[vector].open()

    def blow_up(self):
        self.game_state.is_game_over = True
        for vector in self._mine_vectors:
            self.cells[vector].open()

    def draw(self, screen: pg.Surface):
        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                sprite = pg.transform.scale(cell.get_sprite(), (self.cell_size, self.cell_size))
                screen.blit(sprite, (x * self.cell_size, y * self.cell_size))

    def set_flag(self, vector: Vector):
        self.cells[vector].change_flag()

    def handle_mouse_event(self, pos, button):
        if self.game_state.is_game_over:
            # player can do nothing
            return
        vector = tuple(x // self.cell_size for x in pos)
        if button == pg.BUTTON_LEFT:
            self.expose_cell(vector)
        elif button == pg.BUTTON_RIGHT:
            self.set_flag(vector)

