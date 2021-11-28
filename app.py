import pygame as pg
from settings import *
from gui import *
from canvas import Canvas
from utils import Tools
from colorpicker import Picker
from tools.select import SelectionRect

from os import path
import sys

class Pyx:

    def __init__(self, tile_size: int):
        pg.init()

        # Main screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen_rect = self.screen.get_rect()
        #
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        
        
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
        self.bucket_icon = pg.image.load(path.join(img_folder, BUCKET_ICON)).convert_alpha()
        self.bucket_icon_hover = pg.image.load(path.join(img_folder, BUCKET_HOVER)).convert_alpha()
        self.bucket_icon_clicked = pg.image.load(path.join(img_folder, BUCKET_CLICKED)).convert_alpha()
        self.square_select_icon = pg.image.load(path.join(img_folder, SQUARE_SELECT_ICON)).convert_alpha()
        self.square_select_icon_hover = pg.image.load(path.join(img_folder, SQUARE_SELECT_HOVER)).convert_alpha()
        self.square_select_icon_clicked = pg.image.load(path.join(img_folder, SQUARE_SELECT_CLICKED)).convert_alpha()

    def new(self):
        """ Initialize variables and do the initial setup """

        self.canvas = Canvas(self)
        self.gui = GUI(self)
        self.colorpicker = Picker(self)
        self.tool_buttons = pg.sprite.Group()
        self.load_toolbtns()
        self.selected_tool = self.pencil_tool
        self.selected_tool.clicked = True
        self.selected_color = BLACK
        self.selection_on = False
        self.canvas_grid = []
        for x in range(0, self.tile_size):
            self.canvas_grid.append([])
            for y in range(0, self.tile_size):
                self.canvas_grid[x].append({"color":WHITE})
        
    

    def load_toolbtns(self):
        self.pencil_tool = ToolBtns(self, self.pencil_icon, self.pencil_icon_hover, self.pencil_icon_clicked, 5, 5, Tools.pencil)
        self.erase_tool = ToolBtns(self, self.eraser_icon, self.eraser_icon_hover, self.eraser_icon_clicked, 42, 5, Tools.eraser)
        self.bucket_tool = ToolBtns(self, self.bucket_icon, self.bucket_icon_hover, self.bucket_icon_clicked, 79, 5, Tools.bucket)
        self.square_select_tool = ToolBtns(self, self.square_select_icon, self.square_select_icon_hover, self.square_select_icon_clicked, 5, 42, Tools.select)

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
        # catch all the events here

        for event in pg.event.get():
            mouse_state = pg.mouse.get_pressed()
            x, y = self.get_tile()
            if event.type == pg.QUIT:
                self.quit()

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # event.button = (left, middle, right, wheel up, wheel down)
                if self.selected_tool.tool_type == Tools.pencil and self.canvas.rect.collidepoint(event.pos):
                    print(x, y)
                    self.register_pixel(x, y)
                elif self.selected_tool.tool_type == Tools.eraser and self.canvas.rect.collidepoint(event.pos):
                    print(x, y)
                    self.register_pixel(x, y, draw=False)
                elif self.selected_tool.tool_type == Tools.bucket and self.canvas.rect.collidepoint(event.pos):
                    print(x, y)
                    color = self.screen.get_at(event.pos)
                    neighbors = self.get_surface_to_fill(x, y, color)
                    self.fill(neighbors)
                elif self.selected_tool.tool_type == Tools.select and not self.selection_on and self.canvas.rect.collidepoint(event.pos):
                    x, y = event.pos
                    x -= self.canvas.rect.x
                    y -= self.canvas.rect.y
                    #x = x // self.tile_size
                    #y = y // self.tile_size
                    self.selection = SelectionRect(self, self.canvas.image, (x, y))
                    self.selection_on = True
                # Select a color from the color picker
                if event.button == 1 and self.gui.rect.collidepoint(event.pos):
                    self.selected_color = self.colorpicker.get_color(event.pos)
            elif event.type == pg.MOUSEMOTION:
                if self.selection_on and mouse_state[0]:
                    self.selection.updateRect(event.pos)
                    self.selection.draw(self.canvas.image)
                
                # mouse_state = Bool(left, middle, right)
                if mouse_state[0] and self.selected_tool.tool_type == Tools.pencil and self.canvas.rect.collidepoint(event.pos):
                    print(x, y)
                    self.register_pixel(x, y)
                if mouse_state[0] and self.selected_tool.tool_type == Tools.eraser and self.canvas.rect.collidepoint(event.pos):
                    print(x, y)
                    self.register_pixel(x, y, draw=False)
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if self.selection_on:
                    self.selection_on = False
                    self.selection.updateRect(event.pos)
                    #self.selection.hide(self.canvas.image)


            for btn in self.tool_buttons:
                if btn.rect.collidepoint(pg.mouse.get_pos()):
                    btn.hovered = True
                    if mouse_state[0]:
                        if btn.tool_type != self.selected_tool.tool_type:
                            self.selected_tool.clicked = False
                        self.selected_tool = btn
                        self.selected_tool.clicked = True
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

    def register_pixel(self, x, y, draw=True):
        """ Register new pixels onto the canvas matrix
            Default color is BLACK """
        
        if x is None or y is None:
            return
        try:
            self.canvas_grid[x][y] = {"color":self.selected_color} if draw else {"color":WHITE}
        except IndexError:
            print("Index Error: out of canvas range")

    def fill(self, tiles):
        """ Fills a surface """
        
        for p in tiles:
            for t in p:
                self.register_pixel(t[0], t[1])

    def get_surface_to_fill(self, xpos, ypos, color):
        

        if xpos == None or ypos == None:
            return

        tiles = []
        
        
        for y in reversed(range(ypos + 1)):
            if self.check_color_limits(xpos, y, color):
                tiles.append(self.horizontal_line(xpos, y, color))
                continue
            break
        for y in range(ypos, len(self.canvas_grid)):
            if self.check_color_limits(xpos, y, color):
                tiles.append(self.horizontal_line(xpos, y, color))
                continue
            break
        

        return tiles

    def horizontal_line(self, xpos, ypos, color):
        line = []

        # From starting point to west
        for x in reversed(range(xpos + 1)):
            point = self.canvas_grid[x][ypos]
            if point["color"] == color:
                line.append((x, ypos))
            else:
                break

        # From starting point to east
        for x in range(xpos, len(self.canvas_grid)):
            point = self.canvas_grid[x][ypos]
            if point["color"] == color:
                line.append((x, ypos))
            else:
                break
        
        return line

    def check_color_limits(self, xpos, ypos, color):
        """ checks for color limits """

        point = self.canvas_grid[xpos][ypos]
        if point["color"] == color:
            return True
        return False




    def draw(self):
        self.screen.fill(SCREEN_COLOR)
        self.canvas.draw()
        self.canvas.draw_pixel(self.canvas_grid)
        self.gui.draw()
        self.tool_buttons.update()
        self.tool_buttons.draw(self.screen)
        self.colorpicker.draw(200, 5)
        pg.display.flip()

if __name__ == "__main__":

    tile_size = int(input("Tile Size >> "))
    p = Pyx(tile_size)
    p.new()
    while True:
        p.run()