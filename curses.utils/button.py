import curses

from src.core.render import CursesRenderer

class CursesButton:

    mousex : int
    mousey : int
    posx : int
    posy: int
    sizex: int
    sizey: int

    def __init__(self, renderer : CursesRenderer, posx, posy, sizex, sizey):
        self.posx = posx
        self.posy = posy
        self.sizex = sizex
        self.sizey = sizey

    def check_on_click(self, key : int):
        key = self.renderer.stdscr.getch()
        if key == curses.KEY_MOUSE:
            self.mousex, self.mousey = curses.getmouse()[1], curses.getmouse()[2]
            if self.mousex >= self.posx:
                if self.mousex <= self.posx + self.xsize:
                    if self.mousey >= self.pos_y:
                        if self.mousey <= self.posy + self.ysize:
                            return True

    def draw(self):
        pass