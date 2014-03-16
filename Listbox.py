__author__ = 'thvoidedline'


import pygame
from GuiObject import GuiObject
from Constants import*


class Listbox(GuiObject):
    def __init__(self, name, cords, items_list=None):
        GuiObject.__init__(self, name, cords)
        self.items_dict = {}
        self.update_list(items_list, True)
        self.type = LIST_BOX
        self.selected = 0

    def update_list(self, items_list, changed):
        if changed and items_list:
            self.items_dict.clear()
            for text in items_list:
                print(text)
                img = self.font.render(text, True, (50, 50, 50))
                self.items_dict[text] = img
                size = self.font.size(text)
                width = size[0]
                height = size[1]
                if width > self.w:
                    self.w = width + self.margin
                self.h = (height + 10) * len(self.items_dict)

    def display(self, screen):
        pygame.draw.rect(screen, self.bg_color, (self.cords[X], self.cords[Y], self.w, self.h), 0)

        item_x = self.cords[X]
        item_y = self.cords[Y]
        if self.items_dict:
            index = 0
            for img in self.items_dict.values():
                if index == self.selected:
                    pygame.draw.rect(screen, (200, 200, 200),
                                     (item_x, item_y, img.get_width() + self.margin, img.get_height() + self.margin), 0)
                screen.blit(img, (item_x + self.margin, item_y + self.margin))
                item_y += self.font.get_height() + 10
                index += 1