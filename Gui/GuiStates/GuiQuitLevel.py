from Gui.GuiStates.GuiState import GuiState

__author__ = 'thvoidedline'

from Binding import Binding
from Constants import *


class GuiQuitLevel(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state)
        self.esc_once = False
        self.keybindings.add(LevelQuitBind(pygame.K_ESCAPE, self))
        self.toggle("Quitting")

    def create(self, *args):
        GuiState.create(self, *args)

    def destroy(self, *args):
        GuiState.destroy(self)
        self.keybindings.remove(pygame.K_ESCAPE)

    def quit_game(self):
        if self.esc_once:
            pygame.event.post(pygame.event.Event(QUIT_EVENT))
        else:
            self.esc_once = True

class LevelQuitBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            quit_lvl_gui = self.args[0]
            quit_lvl_gui.quit_game()