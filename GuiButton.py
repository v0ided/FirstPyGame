__author__ = 'thvoidedline'

import pygame
from GuiObject import GuiObject
from Constants import *


class GuiButton(GuiObject):
    def __init__(self, var_dict):
        GuiObject.__init__(self, var_dict)

        try:
            self.font_size = var_dict['font_size']
            self.font_color = var_dict['font_color']
            self.text = var_dict['text']
            self.action = var_dict['action']
            self.bg_color = var_dict['bg_color']
        except KeyError:
            print('Not all required arguments passed to GuiButton')
            raise

        self.font = pygame.font.SysFont("Calibri", self.font_size)
        self.font_img = self.font.render(self.text, True, self.font_color)
        size = self.font.size(self.text)
        self.rect.w = size[0] + (self.margin * 2)
        self.rect.h = size[1] + (self.margin * 2)

    def get_text(self):
        return self.text

    def draw(self, screen):
        #draw button background
        pygame.draw.rect(screen, self.bg_color, self.rect, 0)
        #draw button text
        if self.font_img:
            screen.blit(self.font_img, (self.rect.x + self.margin, self.rect.y + self.margin))

    def input(self, user_input):
        if user_input == pygame.MOUSEBUTTONUP:
            self.action()