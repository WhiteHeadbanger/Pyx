import pygame as pg
from settings import *

class Picker:

    def __init__(self, app):
        self.screen = app.gui.image
        #self.colors = pg.color.THECOLORS
        self.colors = [BLACK, WHITE, RED, GREEN, YELLOW]
        self.tilesize = TILESIZE

    def draw(self, x, y):
        #self.image.fill(GUI_COLOR)
        for color in self.colors:
            pg.draw.rect(self.screen, color, (x, y, self.tilesize, self.tilesize))
            x += 40
            

    def get_color(self, pos):
        """ Returns the color the mouse is pointing at """
        return self.screen.get_at(pos)
