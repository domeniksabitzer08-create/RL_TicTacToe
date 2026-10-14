from dataclasses import dataclass
import pygame
import math

from PIL.ImageChops import screen
from pygame import Vector2


### VECTOR CLASS ###
@dataclass(frozen=True)
class Vector2D:
        x: float
        y: float
        def to_tuple(self):
            return self.x, self.y

        def __add__(self, other):
            # Vector + Vector
            if isinstance(other, Vector2D):
                return Vector2D(self.x + other.x, self.y + other.y)
            elif isinstance(other, (int, float)):
                return Vector2D(self.x * other, self.y * other)
            else:
                return NotImplemented
        def __sub__(self, other):
            # Vector - Vector
            if isinstance(other, Vector2D):
                return Vector2D(self.x - other.x, self.y - other.y)
            else:
                return NotImplemented
        def __mul__(self, other):
            if isinstance(other, (int, float)):
                # Vector * Number
                return Vector2D(self.x * other, self.y * other)
            else:
                return NotImplemented
        def __truediv__(self, other):
            # Vector / Number
            if isinstance(other, (int, float)):
                return Vector2D(self.x / other, self.y / other)
            else:
                return NotImplemented
        def __eq__(self, other):
            if isinstance(other, Vector2D):
                return self.x == other.x and self.y == other.y
            else:
                return NotImplemented
        def magnitude(self):
            return math.sqrt(self.x * self.x + self.y * self.y)


class TicTacToeEnv:
    def __init__(self, render : bool = True):
        # Overall
        self.render = render
        self.game_running = True
        # Design
        self.screen_size = (800, 800)
        self.line_thickness = 10
        self.cell_size = 150
        self.grid_start_pos = Vector2D(100, 25)
        self.line_color = (255,255,255)
        self.tile_padding = 20
        self.circle_color = (0,0,255)
        self.cross_color = (255,0,0)
        self.tile_thickness = 13
        # Instantiate screen
        self.screen = pygame.display.set_mode(self.screen_size)
        # Gameplay
        self.tiles_list = [[None] * 3] * 3

    def start(self):
        print(f"tile list: {self.tiles_list}")
        self.update()

    def update(self):
        while self.game_running:
            self.render_grid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False

    def render_grid(self):
        self.draw_cross(0,0)
        # render vertical lines
        for i in range(4):
            self.render_vertical_line(Vector2D(self.grid_start_pos.x + i * self.cell_size , self.grid_start_pos.y))
        for i in range(4):
            self.render_horizontal_line(Vector2D(self.grid_start_pos.x  , self.grid_start_pos.y + i * self.cell_size))
        pygame.display.update()

    def render_vertical_line(self, line_pos: Vector2D):
        line = pygame.Rect(line_pos.x, line_pos.y, self.line_thickness, self.cell_size*3)
        pygame.draw.rect(self.screen, self.line_color, line)

    def render_horizontal_line(self, line_pos: Vector2D):
        line = pygame.Rect(line_pos.x, line_pos.y, self.cell_size*3 + self.line_thickness, self.line_thickness)
        pygame.draw.rect(self.screen, self.line_color, line)

    def draw_circle(self, row : int, column : int):
        screen_pos = self.grid_to_screen_pos(row, column)
        pygame.draw.circle(self.screen, self.circle_color, screen_pos.to_tuple() , self.cell_size/2 - self.tile_padding, width=self.tile_thickness )

    def draw_cross(self, row : int, column : int):
        line_pos = self.grid_to_screen_pos(row, column)
        start_pos = (
            line_pos.x - self.cell_size / 2 + self.tile_padding, line_pos.y - self.cell_size / 2 + self.tile_padding)
        end_pos = (
            line_pos.x + self.cell_size / 2 - self.tile_padding, line_pos.y + self.cell_size / 2 - self.tile_padding)
        pygame.draw.line(self.screen, self.cross_color, start_pos, end_pos, width=self.tile_thickness)

        start_pos = (
            line_pos.x - self.cell_size / 2 + self.tile_padding, line_pos.y + self.cell_size / 2 - self.tile_padding)
        end_pos = (
            line_pos.x + self.cell_size / 2 - self.tile_padding, line_pos.y - self.cell_size / 2 + self.tile_padding)

        pygame.draw.line(self.screen, self.cross_color, start_pos, end_pos, width=self.tile_thickness)


    def grid_to_screen_pos(self, row: int, column: int):
        world_pos = self.grid_start_pos + Vector2D(self.cell_size/2 + self.cell_size * row,self.cell_size/2 + self.cell_size * column )
        return world_pos

