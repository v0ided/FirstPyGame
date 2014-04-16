__author__ = 'thvoidedline'

import pygame
from Gui.GuiStateNEW import GuiState
from Binding import LevelQuitBind


class GuiQuitLevel(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state, *args)
        self.create(*args)

    def create(self, *args):
        GuiState.create(self, *args)
        self.keybindings.add(LevelQuitBind(pygame.K_ESCAPE, self))

    def destroy(self):
        GuiState.destroy(self)