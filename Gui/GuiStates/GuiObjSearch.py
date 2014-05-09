__author__ = 'thvoidedline'

import pygame
from Gui.GuiStates.GuiState import GuiState
from Binding import Binding
from Binding import ListboxUpBind
from Binding import ListboxDownBind
from Constants import *
from HelpFunctions import search_file


class GuiObjSearch(GuiState):
    def __init__(self, state):
        GuiState.__init__(self, state)
        self.listbox = None
        self.textbox = None
        self.level = None

    def create(self, *args):
        print('Create GuiObjSearch called')
        GuiState.create(self, *args)
        try:
            pygame.mouse.set_visible(False)
            self.level = args[0]
            self.keybindings.add(PrePlaceObjectBind(pygame.MOUSEBUTTONUP, self, self.level))
            self.keybindings.add(PrePlaceObjectBind(pygame.K_RETURN, self, self.level))
            self.keybindings.add(ListboxUpBind(pygame.K_UP, "results", self))
            self.keybindings.add(ListboxDownBind(pygame.K_DOWN, "results", self))
            self.textbox = self.add(TXT_BOX, {'name': "c_obj", 'cords': pygame.mouse.get_pos(),
                                              'bg_color': (255, 255, 255)})
            results_pos = (self.textbox.rect.x, self.textbox.rect.y + self.textbox.rect.h + 25)
            self.listbox = self.add(LIST_BOX, {'name': "results", 'cords': results_pos, 'bg_color': (255, 255, 255)})
            self.textbox.attach(self.listbox)

            self.listbox.update_list(self.get_path_results(), True)
            self.focus(self.textbox)
        except (IndexError, TypeError, LookupError, ValueError):
            print('Failed to create GuiObjSearch')

    def get_path_results(self):
        return search_file(self.level._data_dir, self.textbox.text)

    def destroy(self):
        GuiState.destroy(self)
        print('destroying GuiObjSearch')
        self.keybindings.remove(pygame.MOUSEBUTTONUP)
        self.keybindings.remove(pygame.K_RETURN)
        self.keybindings.remove(pygame.K_UP)
        self.keybindings.remove(pygame.K_DOWN)
        self.controls[:] = []
        self.listbox = None
        self.textbox = None
        self.level = None

    def pre_place_object(self):
        pygame.mouse.set_visible(True)
        pygame.mouse.set_pos((self.textbox.rect.x, self.textbox.rect.y))
        self.level.pre_place_object(self.listbox.get_text())
        self.destroy()

    def update(self):
        GuiState.update(self)
        if self.listbox:
            self.listbox.update_list(self.get_path_results(), True)


class PrePlaceObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        try:
            obj_search = self.args[0]
            obj_search.pre_place_object()
        except IndexError:
            print('Error - Invalid arguments passed to PrePlaceObjectBind')