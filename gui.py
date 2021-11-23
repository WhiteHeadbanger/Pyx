import pygame as pg
from settings import *
from utils import Tools

class GUI:

    """ This is just the background, for now """

    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.image = pg.Surface((GUI_WIDTH, GUI_HEIGHT))
        self.image.convert_alpha()
        self.image.fill(GUI_COLOR)
        self.rect = self.image.get_rect()

    #TODO
    def add_btn(self):
        pass

    def draw(self):
        self.screen.blit(self.image, self.rect)

class ToolBtns(pg.sprite.Sprite):

    def __init__(self, app, base, hover_image, clicked_image, x, y, tool_type: Tools):
        self.groups = app.tool_buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gui_surface = app.gui.image
        self.gui_rect = app.gui.rect
        self.screen = app.screen

        self.base_image = base
        self.hover_image = hover_image
        self.clicked_image = clicked_image

        self.tool_type = tool_type

        self.x = x
        self.y = y
        
        self.image = self.base_image
        self.rect = self.base_image.get_rect()
        self.rect.x = self.gui_rect.x + x
        self.rect.y = self.gui_rect.y + y
        
        self.hovered = False
        self.clicked = False

    def update(self):
        if self.hovered:
            self.image = self.hover_image
        if self.clicked:
            self.image = self.clicked_image
        else:
            self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.x = self.gui_rect.x + self.x
        self.rect.y = self.gui_rect.y + self.y










