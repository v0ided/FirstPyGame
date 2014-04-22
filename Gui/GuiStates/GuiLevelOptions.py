from Gui.GuiStates.GuiState import GuiState

__author__ = 'thvoidedline'

from Constants import *
from Binding import ToggleStateBind


class GuiLevelOptions(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state, *args)
        self.level = args[0]
        self.keybindings.add(ToggleStateBind(pygame.K_TAB, self, self.level))

    def create(self, *args):
        GuiState.create(self, *args)
        try:
            self.add(WINDOW, {'name': "leveloptions", 'cords': (300, 300), 'w': 150, 'h': 195,
                              'bg_color': (0, 0, 0), 'font_color': (234, 234, 234)})
            self.add(TEXT, {'name': "lvloptions", 'cords': (310, 310), 'font_color': (234, 234, 234), 'font_size': 20,
                            'text': "Level Options"})
            self.add(BUTTON, {'name': 'clear_bttn', 'cords': (330, 340), 'bg_color': (255, 255, 255),
                              'font_color': (0, 0, 0), 'font_size': 14, 'text': 'Clear Level', 'action': self.level.clear})
            load_bttn = self.add(BUTTON, {'name': 'load_bttn', 'cords': (330, 380), 'bg_color': (255, 255, 255),
                                          'font_color': (0, 0, 0), 'font_size': 14, 'text': 'Load Level', 'action': self.level.load})
            save_bttn = self.add(BUTTON, {'name': 'save_bttn', 'cords': (330, 420), 'bg_color': (255, 255, 255),
                                          'font_color': (0, 0, 0), 'font_size': 14, 'text': 'Save Level', 'action': self.level.save})
            file_txtbox = self.add(TXT_BOX, {'name': 'saveas_txtbox', 'cords': (330, 460), 'bg_color': (255, 255, 255)})
            file_txtbox.text = self.level._filename

            load_bttn.attach(file_txtbox)
            save_bttn.attach(file_txtbox)
            self.focus(file_txtbox)
        except (IndexError, ValueError, TypeError, KeyError):
            print('Error during creation of GuiLevelOptions')

    def destroy(self, *args):
        GuiState.destroy(self)
        self.controls[:] = []