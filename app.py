import pygame as pg
from settings import *
#from gui import GUI
#from pixel import Px

from os import path
import sys

class Pyxel:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        font_folder = path.join(game_folder, 'fonts')

    def new(self):
        """ Initialize variables and do the initial setup """
        #self.gui = GUI()
        self.canvas = []
        for x in range(0, int(WIDTH / TILESIZE)):
            self.canvas.append([])
            for y in range(0, int(HEIGHT / TILESIZE)):
                self.canvas[x].append(0)
        

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def run(self):
        """ App loop """
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS)
            self.events()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x = event.pos[0] // TILESIZE
                y = event.pos[1] // TILESIZE
                print(x, y)
                self.register_pixel(x, y, exists=self.exists(x, y))

    def register_pixel(self, x, y, exists = False):
        """ Register new pixels onto the canvas matrix """

        if not exists:
            self.canvas[x][y] = 1
            return
        self.canvas[x][y] = 0


    def exists(self, x, y):
        """ Check if a pixel exists or not """

        if self.canvas[x][y] == 1:
            return True
        return False

    def draw_pixel(self):
        """ Draws pixels on the screen """

        for row, data in enumerate(self.canvas):
            for col, px in enumerate(data):
                if px == 1:
                    pg.draw.rect(self.screen, BLACK, pg.Rect(row * TILESIZE, col * TILESIZE, TILESIZE, TILESIZE))

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        #self.gui.draw()
        self.draw_pixel()
        pg.display.flip()

if __name__ == "__main__":

    p = Pyxel()
    p.new()
    while True:
        p.run()