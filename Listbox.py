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
        self.rows = 10
        #index of middle item in entire items_dict
        self.top_index = 0

    def update_list(self, items_list, changed):
        if changed and items_list:
            self.items_dict.clear()
            index = 0
            for text in items_list:
                img = self.font.render(text, True, (0, 0, 0))
                self.items_dict[text] = img
                size = self.font.size(text)
                width = size[0]
                height = size[1]
                if width > self.w:
                    self.w = width - 30
                if index <= self.rows:
                    self.h = (height + 7) * len(self.items_dict)
                index += 1

    def select_next(self):
        if self.selected >= len(self.items_dict) - 1:
            self.selected = 0
        else:
            self.selected += 1

    #get selected text
    def get_selected(self):
        index = 0
        for i in self.items_dict.keys():
            if index == self.selected:
                return i
            index += 1

    def display(self, screen):
        s = pygame.Surface((self.w, self.h))
        s.set_alpha(110)
        s.fill((255, 255, 255))
        screen.blit(s, (self.cords[X], self.cords[Y]))
        item_x = self.cords[X]
        item_y = self.cords[Y]
        if self.items_dict:
            index = 0
            for img in self.items_dict.values():
                if self.selected <= index < self.selected + self.rows:
                    if index == self.selected:
                        pygame.draw.rect(screen, (200, 200, 200),
                                        (item_x, item_y, img.get_width() + self.margin,
                                         img.get_height() + self.margin), 0)
                    screen.blit(img, (item_x + self.margin, item_y + self.margin))
                    item_y += self.font.get_height() + 10
                index += 1

    def get_text(self):
        return self.get_selected()