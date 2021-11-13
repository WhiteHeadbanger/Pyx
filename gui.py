import pygame as pg
from settings import *

class GUI:

    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.background_image = pg.Surface((GUI_WIDTH, GUI_HEIGHT))
        self.background_image.fill(GUI_COLOR)
        self.background_rect = self.background_image.get_rect()
        self.background_rect.x = WIDTH - (WIDTH * 0.2)
        self.background_rect.y = 0

    def draw(self):
        self.screen.blit(self.background_image, self.background_rect)


class ToolBtns(pg.sprite.Sprite):

    def __init__(self, app, image, hover_image, x, y):
        self.groups = app.tool_buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.app = app
        self.screen = app.screen
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.hover_image = hover_image
        self.hover_rect = self.hover_image.get_rect()
        self.hover_rect.x = x
        self.hover_rect.y = y
        
        self.hovered = False

    def draw(self):
        if self.hovered:
            self.screen.blit(self.hover_image, self.hover_rect)
        else:
            self.screen.blit(self.image, self.rect)




