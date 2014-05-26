import pygame
from Constants import *


class GuiObject():
    def __init__(self, var_dict):
        try:
            self.name = var_dict['name']
            cords = var_dict['cords']
            self.rect = pygame.Rect(cords[X], cords[Y], 1, 1)
        except LookupError:
            print("Not all required arguments were passed to GuiObject")
            raise

        self.font_color = (0, 0, 0)
        self.font = pygame.font.SysFont("Calibri", 24)
        self.margin = 5
        self.type = GUI_OBJ
        self.attached = {}  # identifier : value
        self.visible = True
        self.is_focus = False

    def draw(self, screen):
        pass

    def update(self):
        pass

    def attach(self, identifier, value):
        if identifier not in self.attached and value is not None:
            self.attached[identifier] = value
        else:
            print('Invalid GUI object attach: ' + self.name)

    def get_text(self):
        return None

    #provides the ability for a gui object to catch user input
    def input(self, user_input):
        pass



