from Gui.GuiStates.GuiState import GuiState

__author__ = 'thvoidedline'

from Binding import Binding
from Binding import ListboxUpBind
from Binding import ListboxDownBind
from Binding import ToggleStateBind
from Constants import *
from HelpFunctions import search_file


class GuiObjSearch(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state, *args)
        self.listbox = None
        self.textbox = None
        #Toggle state existence, do not remove on destroy (calls GuiObjSearch.toggle())
        self.level = args[0]
        self.data_path = args[1]
        self.keybindings.add(ToggleStateBind(pygame.K_SPACE, self))

    def create(self, *args):
        GuiState.create(self, *args)
        try:
            #Select object from listbox
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
        except (IndexError, TypeError, LookupError, ValueError) as e:
            print('Failed to create GuiObjSearch' + e.error)

    def get_path_results(self):
        return search_file(self.data_path, self.textbox.text)

    def destroy(self):
        GuiState.destroy(self)
        self.keybindings.remove(pygame.MOUSEBUTTONUP)
        self.keybindings.remove(pygame.K_RETURN)
        self.keybindings.remove(pygame.K_UP)
        self.keybindings.remove(pygame.K_DOWN)
        self.controls[:] = []
        self.listbox = None
        print(self.keybindings._bindings)

    def pre_place_object(self):
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