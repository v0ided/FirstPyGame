__author__ = 'thvoidedline'

from GuiObject import GuiObject
from Constants import *
import pygame


class GuiWindow(GuiObject):
    def __init__(self, name, cords, w, h, wnd_color, font_color):
        GuiObject.__init__(self, name, cords, wnd_color, font_color)
        self.type = WINDOW
        self.w = w
        self.h = h

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, (self.cords[X], self.cords[Y], self.w, self.h), 0)