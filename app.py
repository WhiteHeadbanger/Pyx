import pygame as pg
from settings import *
from gui import *
#from pixel import Px

from os import path
import sys

class Pyxel:

    def __init__(self, tile_size: int, canvas_width: int = None, canvas_height: int = None):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.tile_size = tile_size

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        font_folder = path.join(game_folder, 'fonts')

        self.pencil_icon = pg.image.load(path.join(img_folder, PENCIL_ICON)).convert_alpha()
        self.pencil_icon_hover = pg.image.load(path.join(img_folder, PENCIL_HOVER)).convert_alpha()

    def new(self):
        """ Initialize variables and do the initial setup """

        self.tool_buttons = pg.sprite.Group()
        self.gui = GUI(self)
        self.load_toolbtns()
        self.canvas = []
        for x in range(0, int(WIDTH / self.tile_size) if self.canvas_width == None else int(self.canvas_width / self.tile_size)):
            self.canvas.append([])
            for y in range(0, int(WIDTH / self.tile_size) if self.canvas_height == None else int(self.canvas_height / self.tile_size)):
                self.canvas[x].append(0)
        

    def draw_grid(self):
        for x in range(0, WIDTH if self.canvas_width == None else self.canvas_width, self.tile_size):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT if self.canvas_height == None else self.canvas_height))
        for y in range(0, HEIGHT if self.canvas_height == None else self.canvas_height, self.tile_size):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH if self.canvas_width == None else self.canvas_width, y))

    def load_toolbtns(self):
        x = WIDTH - int(WIDTH * 0.2) + 5
        self.pencil_tool = ToolBtns(self, self.pencil_icon, self.pencil_icon_hover, x, 5)
        self.erase_tool = ToolBtns(self, self.pencil_icon, self.pencil_icon_hover, x + 37, 5)
        self.rectangle_tool = ToolBtns(self, self.pencil_icon, self.pencil_icon_hover, x + 37 + 37, 5)
        self.circle_tool = ToolBtns(self, self.pencil_icon, self.pencil_icon_hover, x + 37 + 37 + 37, 5)

    def draw_toolbtns(self):
        self.pencil_tool.draw()
        self.erase_tool.draw()
        self.rectangle_tool.draw()
        self.circle_tool.draw()

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
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                x = event.pos[0] // self.tile_size
                y = event.pos[1] // self.tile_size
                print(x, y)
                self.register_pixel(x, y, exists=self.exists(x, y))
            for toolbtns in self.tool_buttons:
                if toolbtns.rect.collidepoint(pg.mouse.get_pos()):
                    toolbtns.hovered = True
                else:
                    toolbtns.hovered = False

    def register_pixel(self, x, y, exists = False):
        """ Register new pixels onto the canvas matrix """

        if not exists:
            try:
                self.canvas[x][y] = 1
                return
            except IndexError:
                print("Fuera de rango")  
        
        try:
            self.canvas[x][y] = 0
            return
        except IndexError:
            print("Fuera de rango")


    def exists(self, x, y):
        """ Check if a pixel exists or not """
        try:
            if self.canvas[x][y] == 1:
                return True
        except IndexError:
            print("Fuera de rango")
        return False

    def draw_pixel(self):
        """ Draws pixels on the screen """

        for row, data in enumerate(self.canvas):
            for col, px in enumerate(data):
                if px == 1:
                    pg.draw.rect(self.screen, BLACK, pg.Rect(row * self.tile_size, col * self.tile_size, self.tile_size, self.tile_size))

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.gui.draw()
        self.draw_toolbtns()
        self.draw_pixel()
        pg.display.flip()

if __name__ == "__main__":

    w = int(input("Canvas Width >> "))
    h = int(input("Canvas Height >> "))
    tile = int(input("Tile Size >> "))
    p = Pyxel(tile, w, h)
    p.new()
    while True:
        p.run()