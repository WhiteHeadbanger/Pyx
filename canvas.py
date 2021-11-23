import pygame as pg
from settings import *

class Canvas:

    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.image = pg.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center = app.screen_rect.center)

    def draw(self):
        self.grid()
        self.screen.blit(self.image, self.rect)

    def grid(self):
        for x in range(0, CANVAS_WIDTH, TILESIZE):
            pg.draw.line(self.image, LIGHTGREY, (x, 0), (x, self.rect.bottom))
        for y in range(0, CANVAS_HEIGHT, TILESIZE):
            pg.draw.line(self.image, LIGHTGREY, (0, y), (self.rect.right, y))

    def draw_pixel(self, canvas_data):
        """ Draws pixels on the screen """

        for row, data in enumerate(canvas_data):
            for col, px in enumerate(data):
                if px:
                    color = px["color"] if px["status"] else (255, 255, 255)
                    rect = pg.Rect(row * self.app.tile_size, col * self.app.tile_size, self.app.tile_size, self.app.tile_size)
                    pg.draw.rect(self.image, color, rect)