from Gui.GuiObject import GuiObject

__author__ = 'thvoidedline'

from Constants import *


class Textbox(GuiObject):
    def __init__(self, var_dict):
        GuiObject.__init__(self, var_dict)
        self.text = ""
        self.img = None
        self.type = TXT_BOX
        self.changed = True
        self.font = pygame.font.SysFont("Calibri", 18)

        try:
            self.bg_color = var_dict['bg_color']
        except KeyError:
            print("Not all required arguments given to Textbox")
            raise

    def str_input(self, str_input, replace=False):
        if replace:
            self.text = str_input
        else:
            self.text += str_input
        self.changed = True

    def input(self, chr_input):
        if chr_input == pygame.K_BACKSPACE:
            self.backspace()
        elif chr_input == pygame.K_SPACE:
            return
        elif pygame.K_ESCAPE < chr_input < pygame.K_DELETE:
            self.text += chr(chr_input)
        self.changed = True

    def update(self):
        if self.changed:
            size = self.font.size(self.text)
            self.rect.w = size[0] + (self.margin * 2)
            self.rect.h = size[1]
            self.img = self.font.render(self.text, True, self.font_color)
            self.changed = False

    def backspace(self):
        if len(self.text) > 0:
            self.text = self.text[:-1]
            self.changed = True

    def draw(self, screen):
        if self.is_focus:
            pygame.draw.rect(screen, (180, 180, 180), self.rect, 0)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect, 0)
        if self.img is not None:
            screen.blit(self.img, self.rect)

    def get_text(self):
        return self.text