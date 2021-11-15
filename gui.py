import pygame as pg
from settings import *
from utils import Tools

class GUI:

    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.background_image = pg.Surface((GUI_WIDTH, GUI_HEIGHT))
        self.background_image.fill(GUI_COLOR)
        self.background_rect = self.background_image.get_rect()
        self.background_rect.x = WIDTH - (WIDTH * 0.1)
        self.background_rect.y = 0

    def draw(self):
        self.screen.blit(self.background_image, self.background_rect)


class ToolBtns(pg.sprite.Sprite):

    def __init__(self, app, image, hover_image, clicked_image, x, y, tool_type: Tools):
        self.groups = app.tool_buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.app = app
        self.gui_surface = app.gui.background_image
        #self.screen = app.screen
        self.tool_type = tool_type
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.hover_image = hover_image
        self.hover_rect = self.hover_image.get_rect()
        self.hover_rect.x = x
        self.hover_rect.y = y

        self.clicked_image = clicked_image
        self.clicked_rect = self.hover_image.get_rect()
        self.clicked_rect.x = x
        self.clicked_rect.y = y
        
        self.hovered = False
        self.clicked = False


    def draw(self):
        if self.hovered:
            self.gui_surface.blit(self.hover_image, self.hover_rect)
        elif self.clicked:
            self.gui_surface.blit(self.clicked_image, self.clicked_rect)
        else:
            self.gui_surface.blit(self.image, self.rect)





