# level.py
import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type="solid"):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        if tile_type == "solid":
            self.image.fill((100, 100, 100))  # sol/mur
        else:
            self.image.fill((50, 50, 50))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.tile_type = tile_type

class Level:
    def __init__(self, layout):
        self.tiles = pygame.sprite.Group()
        self.load_layout(layout)

    def load_layout(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == "X":
                    tile = Tile(x, y, "solid")
                    self.tiles.add(tile)

    def draw(self, surface):
        self.tiles.draw(surface)


LEVEL_1_LAYOUT = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                              ",
    "X                                              ",
    "X                                              ",
    "X                                              ",
    "X                                              ",
    "X                                              ",
    "X                                              ",
    "X                                              ",
    "X                                              ",
    "X                                              ",
    "X                                              ",
    "X                       X                      ",
    "X                       X                     X",
    "X                          X                  X",
    "X                          X            X     X",
    "X                                        XXXXXX",
    "X              XXX                    X       X",
    "X                      X                      X",
    "X        XXX                       X          X",
    "X                                 X           X",
    "X  XXX                 XXX     XXXXXXXXXXXXXX X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX X",
]
