import pygame as pg
from pygame.locals import *
import copy

class SelectionRect:
    """ class SelectionRect utility class for using selection rectangles"""
    def __init__(self, app, screen, start, col = (0, 0, 0)):
        """ __init__(self,screen,start,col=(0,0,0))
        Constructor. Pass starting point of selection rectangle in 'start'
        and color value in which the selection rectangle shall be drawn
        in 'col'
        """
        self.app = app
        self.canvas = app.canvas
        self.start = start
        self.last_pos = start
        self.col = col
        self.oldrect = start[0] // app.tile_size ,start[1] // app.tile_size ,1,1
        tmp = screen.get_at((start[0] // app.tile_size, start[1] // app.tile_size))[:3]
        self.screen_backup = [[tmp], [tmp], [tmp], [tmp]]
        
    def updateRect(self, now):
        """ updateRect(self,now) -> rect tuple
        This returns a rectstyle tuple describing the selection rectangle
        between the starting point (passed to __init__) and the 'now' edge and
        updates the internal rectangle information for correct drawing.
        """
        x, y = self.start
        mx, my = now
        self.last_pos = (mx, my)
        mx -= self.canvas.rect.x
        my -= self.canvas.rect.y
        if mx > 1024:
            mx = 1024
        if mx < 0:
            mx = 0
        if my > 1024:
            my = 1024
        if my < 0:
            my = 0
        if mx < x:
            if my < y:
                self.rect = mx, my, x - mx, y - my
            else:
                self.rect = mx, y, x - mx, my - y
        elif my < y:
            self.rect = x, my, mx - x, y - my
        else:
            self.rect = x, y, mx - x, my - y
        return self.rect

    def draw(self, screen):
        """ draw(self,screen)
        This hides the old selection rectangle and draws the current one
        """
        # just some shortcuts :P
        surf =  pg.surfarray.pixels3d(screen)
        r    = self.rect
        # hide selection rectangle
        self.hide(screen)
        
        # update background information
        self.screen_backup[0] = copy.copy(surf[r[0]:r[0] + r[2], r[1]])
        self.screen_backup[1] = copy.copy(surf[r[0]:r[0] + r[2], r[1] + r[3] - 1])
        self.screen_backup[2] = copy.copy(surf[r[0], r[1]:r[1] + r[3]])
        self.screen_backup[3] = copy.copy(surf[r[0] + r[2] - 1, r[1]:r[1] + r[3]])

        # draw selection rectangle:
        surf[r[0]:r[0] + r[2], r[1]] = self.col
        surf[r[0]:r[0] + r[2], r[1] + r[3] - 1] = self.col
        surf[r[0], r[1]:r[1] + r[3]] = self.col
        surf[r[0]+ r[2] - 1, r[1]:r[1] + r[3]] = self.col

        self.oldrect = r
        
        #pg.display.update(r)

    def hide(self, screen):
        """ hide(self,screen)
        This hides the selection rectangle using the stored background
        information. You usually call this after you're finished with the
        selection to hide the last rectangle.
        """
        surf = pg.surfarray.pixels3d(screen)
        x, y, x2, y2 = self.oldrect[0], self.oldrect[1],\
                    self.oldrect[0] + self.oldrect[2],\
                    self.oldrect[1] + self.oldrect[3]
        surf[x:x2, y] = self.screen_backup[0]
        surf[x:x2, y2 - 1] = self.screen_backup[1]
        surf[x, y:y2] = self.screen_backup[2]
        surf[x2 - 1, y:y2] = self.screen_backup[3]
        
        
        #pg.display.update(self.oldrect)