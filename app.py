import pygame as pg
from settings import *
from gui import *
#from pixel import Px

from os import path
import sys

class Pyxel:

    def __init__(self, tile_size: int):
        pg.init()
        # SCREENS #
        # Main screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.draw_screen_w = WIDTH - int((WIDTH * 0.2))
        self.draw_screen_h = HEIGHT 
        
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
        for x in range(0, self.tile_size * self.tile_size):
            self.canvas.append([])
            for y in range(0, self.tile_size * self.tile_size):
                self.canvas[x].append(0)
        

    def draw_grid(self):
        for x in range(0, WIDTH if self.draw_screen_w == None else self.draw_screen_w, self.tile_size):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT if self.draw_screen_h == None else self.draw_screen_h))
        for y in range(0, HEIGHT if self.draw_screen_h == None else self.draw_screen_h, self.tile_size):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH if self.draw_screen_w == None else self.draw_screen_w, y))

    def load_toolbtns(self):
        w = WIDTH - int(WIDTH * 0.2) + 5
        self.pencil_tool = ToolBtns(self, self.pencil_icon, self.pencil_icon_hover, w, 5)
        w += 37
        self.erase_tool = ToolBtns(self, self.pencil_icon, self.pencil_icon_hover, w, 5)
        w += 37
        self.rectangle_tool = ToolBtns(self, self.pencil_icon, self.pencil_icon_hover, w, 5)
        w += 37
        self.circle_tool = ToolBtns(self, self.pencil_icon, self.pencil_icon_hover, w, 5)

    def draw_toolbtns(self):
        self.pencil_tool.draw()
        self.erase_tool.draw()
        self.rectangle_tool.draw()
        self.circle_tool.draw()

    def run(self):
        """ App loop """
        self.running = True
        while self.running:
            self.dt = self.clock.tick()
            self.draw()
            self.events()

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            mouse_state = pg.mouse.get_pressed()
            x, y = self.get_mouse_tile()
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Left click
                if event.button == 1: #and self.selected_tool == Tools.Pencil:
                    print(x, y)
                    self.register_pixel(x, y, color=BLACK)
                # Right click
                if event.button == 3: #and self.selected_tool == Tools.Pencil:
                    print(x, y)
                    self.register_pixel(x, y, color=RED)
            elif event.type == pg.MOUSEMOTION:
                # Left click
                if mouse_state[0]: #and self.selected_tool == Tools.Pencil:
                    print(x, y)
                    self.register_pixel(x, y, color=BLACK)
                # Right click
                if mouse_state[2]: #and self.selected_tool == Tools.Pencil:
                    print(x, y)
                    self.register_pixel(x, y, color=RED)

            # Hover on tool buttons
            for toolbtns in self.tool_buttons:
                if toolbtns.rect.collidepoint(pg.mouse.get_pos()):
                    toolbtns.hovered = True
                else:
                    toolbtns.hovered = False

    def get_mouse_tile(self):
        """ Returns the tile that the mouse is pointing """

        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        x, y = [int(v // self.tile_size) for v in mouse_pos]
        if x >= 0 and y >= 0:
            return (x, y)

    def register_pixel(self, x, y, color):
        """ Register new pixels onto the canvas matrix """

        if not self.exists(x, y):
            try:
                self.canvas[x][y] = {"color":color, "status":1}
                return
            except IndexError:
                print("Fuera de rango")  
    
    def unregister_pixel(self, x, y):
        """ Unregister a pixel from the canvas matrix """

        if self.exists(x, y):
            try:
                self.canvas[x][y] = 0
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
                if px:
                    if px["status"] == 1:
                        pg.draw.rect(self.screen, px["color"], pg.Rect(row * self.tile_size, col * self.tile_size, self.tile_size, self.tile_size))

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_pixel()
        self.gui.draw()
        self.draw_toolbtns()
        pg.display.flip()

if __name__ == "__main__":

    
    tile = int(input("Tile Size >> "))
    p = Pyxel(tile)
    p.new()
    while True:
        p.run()