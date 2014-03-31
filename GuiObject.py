import pygame
from Constants import *


class GuiObject():
    def __init__(self, name, cords, wnd_color, font_color):
        self.name = name
        self.cords = cords
        self.font = pygame.font.SysFont("Calibri", 24)
        self.w = 0
        self.h = 0
        self.margin = 5
        self.bg_color = wnd_color
        self.font_color = font_color
        self.type = GUI_OBJ
        self.attached = []
        self.visible = True

    def draw(self, screen):
        pass

    def update(self):
        pass

    def attach(self, to_be):
        if to_be not in self.attached and to_be is not None:
            self.attached.append(to_be)
        else:
            print('Invalid GUI object attach: ' + self.name)

    def get_text(self):
        return None

    #provides the ability for a gui object to catch user input
    def input(self, key):
        pass



