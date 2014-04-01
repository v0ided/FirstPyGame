__author__ = 'thvoidedline'

from GuiObject import GuiObject
from Constants import *
import pygame


class GuiWindow(GuiObject):
    def __init__(self, var_dict):
        GuiObject.__init__(self, var_dict)
        self.type = WINDOW
        try:
            self.rect.w = var_dict['w']
            self.rect.h = var_dict['h']
            self.bg_color = var_dict['bg_color']
        except KeyError:
            print("Not all required arguments given to GuiWindow")
            raise

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, 0)