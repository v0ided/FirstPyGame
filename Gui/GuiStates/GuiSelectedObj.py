from Gui.GuiStates.GuiState import GuiState

__author__ = 'thvoidedline'

from Binding import Binding
from Binding import DeleteObjectBind
from Constants import *


class GuiSelectedObj(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state, *args)
        self.create(*args)

    def create(self, *args):
        GuiState.create(self, *args)
        try:
            self.keybindings.add(SelectObjectBind(pygame.MOUSEBUTTONUP, args[0].mouse_click))
            self.level = args[0]

        except IndexError:
            print('Error during creation of GuiSelectedObj')

    def destroy(self):
        GuiState.destroy(self)
        self.keybindings.remove(pygame.MOUSEBUTTONUP)


class SelectObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            self.args[0]()
