import pygame as pg
from settings import *
from gui import *
from canvas import Canvas
from utils import Tools

from os import path
import sys

class Pyxel:

    def __init__(self, tile_size: int):
        pg.init()
        # SCREENS #
        # Main screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen_rect = self.screen.get_rect()
        #
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.draw_screen_w = WIDTH - GUI_WIDTH
        self.draw_screen_h = HEIGHT 
        
        self.tile_size = tile_size

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        font_folder = path.join(game_folder, 'fonts')

        self.pencil_icon = pg.image.load(path.join(img_folder, PENCIL_ICON)).convert_alpha()
        self.pencil_icon_hover = pg.image.load(path.join(img_folder, PENCIL_HOVER)).convert_alpha()
        self.pencil_icon_clicked = pg.image.load(path.join(img_folder, PENCIL_CLICKED)).convert_alpha()
        self.eraser_icon = pg.image.load(path.join(img_folder, ERASER_ICON)).convert_alpha()
        self.eraser_icon_hover = pg.image.load(path.join(img_folder, ERASER_HOVER)).convert_alpha()
        self.eraser_icon_clicked = pg.image.load(path.join(img_folder, ERASER_CLICKED)).convert_alpha()

    def new(self):
        """ Initialize variables and do the initial setup """

        self.canvas = Canvas(self)
        self.tool_buttons = pg.sprite.Group()
        self.gui = GUI(self)
        self.load_toolbtns()
        self.selected_tool = self.pencil_tool
        self.selected_color = BLACK
        self.canvas_grid = []
        for x in range(0, self.tile_size):
            self.canvas_grid.append([])
            for y in range(0, self.tile_size):
                self.canvas_grid[x].append({"color":None, "status":0})
        
    

    def load_toolbtns(self):
        self.pencil_tool = ToolBtns(self, self.pencil_icon, self.pencil_icon_hover, self.pencil_icon_clicked, 5, 5, Tools.pencil)
        self.erase_tool = ToolBtns(self, self.eraser_icon, self.eraser_icon_hover, self.eraser_icon_clicked, 42, 5, Tools.eraser)

    def draw_toolbtns(self):
        self.pencil_tool.draw()
        self.erase_tool.draw()

    def run(self):
        """ App loop """
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS)
            self.draw()
            self.events()

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            mouse_state = pg.mouse.get_pressed()
            x, y = self.get_tile()
            if event.type == pg.QUIT:
                self.quit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                # event.button = (left, middle, right, wheel up, wheel down)
                if event.button == 1: #and self.selected_tool.tool_type == Tools.pencil:
                    print(x, y)
                    self.register_pixel(x, y, color=self.selected_color)
                """ if event.button == 1: #and self.selected_tool.tool_type == Tools.eraser:
                    print(x, y)
                    self.unregister_pixel(x, y) """
            elif event.type == pg.MOUSEMOTION:
                # mouse_state = Bool(left, middle, right)

                """ for btn in self.tool_buttons:
                    if btn.rect.collidepoint(pg.mouse.get_pos()):
                        btn.hovered = True
                        if mouse_state[0]:
                            if btn.tool_type != self.selected_tool.tool_type:
                                self.selected_tool.clicked = False
                            btn.clicked = True
                            self.selected_tool = btn
                    else:
                        btn.hovered = False """

                if mouse_state[0]: #and self.selected_tool.tool_type == Tools.pencil:
                    print(x, y)
                    self.register_pixel(x, y, color=self.selected_color)
                """ if mouse_state[0]: #and self.selected_tool.tool_type == Tools.eraser:
                    print(x, y)
                    self.unregister_pixel(x, y) """

            for btn in self.tool_buttons:
                if btn.rect.collidepoint(pg.mouse.get_pos()):
                    btn.hovered = True
                else:
                    btn.hovered = False

    def get_tile(self):
        """ Returns the tile that the mouse is pointing """

        x, y = pg.mouse.get_pos()
        x -= self.canvas.rect.x
        y -= self.canvas.rect.y
        dx = x // self.tile_size
        dy = y // self.tile_size
        if (dx >= 0 and dy >= 0) and (dx <= self.tile_size - 1 and dy <= self.tile_size - 1):
            return (dx, dy)
        return None, None

    def register_pixel(self, x, y, color):
        """ Register new pixels onto the canvas matrix """
        if x is None or y is None:
            return
        try:
            self.canvas_grid[x][y] = {"color":color, "status":True}
        except IndexError:
            print("Fuera de rango")
    
    def unregister_pixel(self, x, y):
        """ Unregister a pixel from the canvas matrix """
        if x is None or y is None:
            return
        try:
            self.canvas_grid[x][y] = {"color":None, "status":False}
        except IndexError:
            print("Fuera de rango")

    def draw_pixel(self):
        """ Draws pixels on the screen """

        for row, data in enumerate(self.canvas_grid):
            for col, px in enumerate(data):
                if px:
                    if px["status"]:
                        pg.draw.rect(self.canvas.image, px["color"], pg.Rect(row * self.tile_size, col * self.tile_size, self.tile_size, self.tile_size))

    def draw(self):
        self.screen.fill(SCREEN_COLOR)
        self.canvas.draw()
        self.gui.draw()
        self.draw_toolbtns()
        self.draw_pixel()
        pg.display.flip()

if __name__ == "__main__":

    tile_size = int(input("Tile Size >> "))
    p = Pyxel(tile_size)
    p.new()
    while True:
        p.run()