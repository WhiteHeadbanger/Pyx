import pygame as pg
from settings import *

class Canvas:

    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.image = pg.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=app.screen_rect.center)

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.grid()

    def grid(self):
        for x in range(0, CANVAS_WIDTH, self.app.tile_size):
            pg.draw.line(self.image, LIGHTGREY, (x, 0), (x, self.rect.bottom))
        for y in range(0, CANVAS_HEIGHT, self.app.tile_size):
            pg.draw.line(self.image, LIGHTGREY, (0, y), (self.rect.right, y))