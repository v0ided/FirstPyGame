from Gui.GuiObject import GuiObject
import pygame
__author__ = 'thvoidedline'

from Constants import *


class GuiListbox(GuiObject):
    def __init__(self, var_dict):
        GuiObject.__init__(self, var_dict)
        self.items_dict = {}
        self.type = LIST_BOX
        try:
            self.bg_color = var_dict['bg_color']
            if 'items_list' in var_dict:
                self.update_list(var_dict['items_list'], True)
        except KeyError:
            print("Not all required argumennts given to GuiListbox")
            raise

        self.selected = 0
        self.rows = 10
        #index of middle item in entire items_dict
        self.top_index = 0

    def update_list(self, items_list, changed):
        if changed and items_list:
            self.items_dict.clear()
            #self.selected = 0
            index = 0
            for text in items_list:
                img = self.font.render(text, True, self.font_color)
                self.items_dict[text] = img
                width, height = self.font.size(text)
                if width > self.rect.w:
                    self.rect.w = width - 30
                if index <= self.rows:
                    self.rect.h = (height + 7) * len(self.items_dict)
                index += 1

    #direction must be a value of 0(DIR_UP) or 1(DIR_DOWN)
    def select_next(self, direction):
        if direction == DIR_UP:
            if self.selected < 0:
                self.selected = len(self.items_dict) - 1
            else:
                print(self.selected)
                self.selected -= 1
        elif direction == DIR_DOWN:
            if self.selected > len(self.items_dict) - 1:
                self.selected = 0
            else:
                self.selected += 1

    #get selected text
    def get_selected(self):
        index = 0
        for key in self.items_dict.keys():
            if index == self.selected:
                return key
            index += 1

    def draw(self, screen):
        s = pygame.Surface((self.rect.w, self.rect.h))
        s.set_alpha(110)
        s.fill(self.bg_color)
        screen.blit(s, (self.rect.x, self.rect.y))
        #Starting point for item x,y
        item_x, item_y = self.rect.topleft
        if self.items_dict:
            item_imgs = self.items_dict.values()
            for index, img in enumerate(item_imgs):
                # If the index equals selected or resides after selected
                # and is less than the amount of rows after selected
                if self.selected <= index < self.selected + self.rows:
                    #if item is currently selected, draw a special box around it
                    if index == self.selected:
                        pygame.draw.rect(screen, (200, 200, 200),
                                        (item_x, item_y,
                                         img.get_width() + self.margin,
                                         img.get_height() + self.margin), 0)
                    #draw item text
                    screen.blit(img, (item_x + self.margin, item_y + self.margin))
                    item_y += self.font.get_height() + 10

    def get_text(self):
        return self.get_selected()