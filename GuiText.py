__author__ = 'thvoidedline'

import pygame
from GuiObject import GuiObject
from Constants import *


class GuiText(GuiObject):
    def __init__(self,  name, cords, font_color, font_size, text):
        GuiObject.__init__(self, name, cords, (0, 0, 0), font_color)
        self.type = TEXT
        self.font_size = font_size
        self.text = text
        self.font = pygame.font.SysFont("Calibri", font_size)
        self.font_img = self.font.render(self.text, True, self.font_color)

    def draw(self, screen):
        if self.font_img:
            screen.blit(self.font_img, (self.cords[X] + self.margin, self.cords[Y] + self.margin))