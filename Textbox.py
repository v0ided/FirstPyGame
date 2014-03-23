__author__ = 'thvoidedline'

import pygame
from HelpFunctions import search_file
from GuiObject import GuiObject
from Constants import *


class Textbox(GuiObject):
    def __init__(self, name, cords):
        GuiObject.__init__(self, name, cords)
        self.text = ""
        self.img = None
        self.type = TXT_BOX
        self.changed = True

    def get(self, character):
        if character == pygame.K_BACKSPACE:
            self.backspace()
        elif pygame.K_ESCAPE < character < pygame.K_DELETE:
            self.text += chr(character)
        self.changed = True

    def update(self):
        results = search_file(self.text)
        if self.attached:
            self.attached[0].update_list(results, self.changed)
        if self.changed:
            size = self.font.size(self.text)
            self.w = size[0] + (self.margin * 2)
            self.h = size[1] + (self.margin * 2)
            self.img = self.font.render(self.text, True, self.font_color)
            self.changed = False

    def backspace(self):
        if len(self.text) > 0:
            self.text = self.text[:-1]
            self.changed = True

    def display(self, screen):
        pygame.draw.rect(screen, self.bg_color, (self.cords[X], self.cords[Y], self.w, self.h), 0)
        if self.img is not None:
            screen.blit(self.img, (self.cords[X] + self.margin, self.cords[Y] + self.margin))

    def get_text(self):
        return self.text