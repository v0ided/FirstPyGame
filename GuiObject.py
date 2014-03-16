import pygame
from Constants import *


class GuiObject():
    def __init__(self, name, cords):
        self.name = name
        self.cords = cords
        self.font = pygame.font.SysFont("Calibri", 36)
        self.w = 0
        self.h = 0
        self.margin = 5
        self.bg_color = (225, 225, 225)
        self.font_color = (0, 0, 0)
        self.type = GUI_OBJ
        self.attached = []

    def display(self, screen):
        pass

    def update(self):
        pass

    def attach(self, to_be):
        if to_be not in self.attached and to_be is not None:
            self.attached.append(to_be)



