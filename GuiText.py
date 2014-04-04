__author__ = 'thvoidedline'

import pygame
from GuiObject import GuiObject
from Constants import *


class GuiText(GuiObject):
    def __init__(self,  var_dict):
        #Width and height will be set once font is rendered
        GuiObject.__init__(self, var_dict)
        self.type = TEXT

        try:
            self.font_size = var_dict['font_size']
            self.text = var_dict['text']
            self.font_color = var_dict['font_color']
            self.watch_func = var_dict['watch']
        except KeyError:
            print('Not all required arguments passed to GuiText')
            raise

        self.font = pygame.font.SysFont("Calibri", self.font_size)
        if callable(self.watch_func):
            self.font_img = self.font.render(self.text + self.watch_func(), True, self.font_color)
        else:
            self.font_img = self.font.render(self.text + self.watch_func, True, self.font_color)

        self.rect.w, self.rect.h = self.font.size(self.text)

    def get_text(self):
        return self.text

    def draw(self, screen):
        if self.font_img:
            screen.blit(self.font_img, self.rect)

    def update(self):
        if self.watch_func:
            self.font_img = self.font.render(self.text + self.watch_func(), True, self.font_color)