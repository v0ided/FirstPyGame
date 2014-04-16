__author__ = 'thvoidedline'

from Gui.GuiStateNEW import GuiState
from Binding import SelectObjectBind
from Binding import DeleteObjectBind
from Constants import *


class GuiSelectedObj(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state, *args)
        self.create(*args)

    def create(self, *args):
        GuiState.create(self, *args)
        try:
            level = args[0]
            #mousebutton -> level.place_object
            self.keybindings.add(SelectObjectBind(pygame.MOUSEBUTTONUP, level))
            self.keybindings.add(DeleteObjectBind(pygame.K_F6, level))

        except IndexError:
            print('Error during creation of GuiSelectedObj')

    def destroy(self):
        GuiState.destroy(self)
        self.keybindings.remove(pygame.MOUSEBUTTONUP)
        self.keybindings.remove(pygame.K_F6)