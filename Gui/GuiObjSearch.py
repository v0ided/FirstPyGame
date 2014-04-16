__author__ = 'thvoidedline'

from Gui.GuiStateNEW import GuiState
from Binding import PrePlaceObjectBind
from Binding import ListboxUpBind
from Binding import ListboxDownBind
from Binding import ToggleStateBind
from Constants import *
from HelpFunctions import search_file


class GuiObjSerach(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state, *args)
        self.create(*args)
        self.listbox = None

    def create(self, *args):
        GuiState.create(self, *args)
        try:
            level = args[0]
            data_path = args[1]
            #Toggle binding, do not remove on destroy (calls GuiObjSearch.toggle())
            self.keybindings.add(ToggleStateBind(pygame.K_SPACE, self))
            #Select object from listbox
            self.keybindings.add(PrePlaceObjectBind(pygame.MOUSEBUTTONUP, self, level))
            self.keybindings.add(PrePlaceObjectBind(pygame.K_RETURN, self, level))
            self.keybindings.add(ListboxUpBind(pygame.K_UP, "results", self))
            self.keybindings.add(ListboxDownBind(pygame.K_DOWN, "results", self))
            textbox = self.add(OBJ_S_TXT_BOX, {'name': "c_obj", 'cords': pygame.mouse.get_pos(),
                                               'bg_color': (255, 255, 255)})
            results_pos = (textbox.rect.x, textbox.rect.y + textbox.rect.h + 25)
            self.listbox = self.add(LIST_BOX, {'name': "results", 'cords': results_pos, 'bg_color': (255, 255, 255)})
            textbox.attach(self.listbox)

            results = search_file(data_path, textbox.text)
            self.listbox.update_list(results, True)
            self.focus(textbox)
        except (IndexError, TypeError, LookupError, ValueError):
            print('Failed to create GuiObjSearch')

    def destroy(self):
        GuiState.destroy(self)
        self.keybindings.remove(pygame.MOUSEBUTTONUP)
        self.keybindings.remove(pygame.K_RETURN)
        self.keybindings.remove(pygame.K_UP)
        self.keybindings.remove(pygame.K_DOWN)
        del self.controls[:]
        del self.listbox

    def pre_place_object(self, level):
        level.pre_place_obj(self.listbox.get_text())