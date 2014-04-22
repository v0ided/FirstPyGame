from Gui.GuiStates.GuiState import GuiState

__author__ = 'thvoidedline'

from Binding import Binding
from Constants import *


class GuiQuitLevel(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state, *args)
        self.esc_once = False
        self.test = args[0]
        self.keybindings.add(LevelQuitBind(pygame.K_ESCAPE, self))
        self.toggle("Quitting")

    def create(self, *args):
        GuiState.create(self, *args)
        self.test = args[0]

    def destroy(self, *args):
        GuiState.destroy(self)
        self.keybindings.remove(pygame.K_ESCAPE)
        self.test = None

    def quit_game(self):
        if self.esc_once:
            pygame.event.post(pygame.event.Event(QUIT_EVENT))
        else:
            self.esc_once = True
        print(self.test)


class LevelQuitBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            quit_lvl_gui = self.args[0]
            quit_lvl_gui.quit_game()