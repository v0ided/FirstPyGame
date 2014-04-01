__author__ = 'thvoidedline'

import pygame
from HelpFunctions import search_file
from GuiObject import GuiObject
from Constants import *


class Textbox(GuiObject):
    def __init__(self, var_dict):
        GuiObject.__init__(self, var_dict)
        self.text = ""
        self.img = None
        self.type = TXT_BOX
        self.changed = True

        try:
            self.bg_color = var_dict['bg_color']
        except KeyError:
            print("Not all required arguments given to Textbox")
            raise

    def input(self, key):
        if key == pygame.K_BACKSPACE:
            self.backspace()
        elif key == pygame.K_SPACE:
            return
        elif pygame.K_ESCAPE < key < pygame.K_DELETE:
            self.text += chr(key)
        self.changed = True

    #todo: This code doesn't belong in a general textbox gui object
    def update(self):
        results = search_file(self.text)
        if self.attached:
            self.attached[0].update_list(results, self.changed)
        if self.changed:
            size = self.font.size(self.text)
            self.rect.w = size[0] + (self.margin * 2)
            self.rect.h = size[1] + (self.margin * 2)
            self.img = self.font.render(self.text, True, self.font_color)
            self.changed = False

    def backspace(self):
        if len(self.text) > 0:
            self.text = self.text[:-1]
            self.changed = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, 0)
        if self.img is not None:
            screen.blit(self.img, self.rect)

    def get_text(self):
        return self.text