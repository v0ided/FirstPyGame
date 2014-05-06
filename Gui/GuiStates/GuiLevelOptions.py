__author__ = 'thvoidedline'

from Gui.GuiStates.GuiState import GuiState
from Constants import *


class GuiLevelOptions(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state)

    def create(self, *args):
        GuiState.create(self, *args)
        level = args[0]
        try:
            self.add(WINDOW, {'name': "leveloptions", 'cords': (300, 300), 'w': 150, 'h': 195,
                              'bg_color': (0, 0, 0), 'font_color': (234, 234, 234)})
            self.add(TEXT, {'name': "lvloptions", 'cords': (310, 310), 'font_color': (234, 234, 234), 'font_size': 20,
                            'text': "Level Options"})
            self.add(BUTTON, {'name': 'clear_bttn', 'cords': (330, 340), 'bg_color': (255, 255, 255),
                              'font_color': (0, 0, 0), 'font_size': 14, 'text': 'Clear Level',
                              'action': level.clear, 'close_state': True})
            load_bttn = self.add(BUTTON, {'name': 'load_bttn', 'cords': (330, 380), 'bg_color': (255, 255, 255),
                                          'font_color': (0, 0, 0), 'font_size': 14, 'text': 'Load Level',
                                          'action': level.load, 'close_state': True})
            save_bttn = self.add(BUTTON, {'name': 'save_bttn', 'cords': (330, 420), 'bg_color': (255, 255, 255),
                                          'font_color': (0, 0, 0), 'font_size': 14, 'text': 'Save Level',
                                          'action': level.save, 'close_state': True})
            file_txtbox = self.add(TXT_BOX, {'name': 'saveas_txtbox', 'cords': (330, 460), 'bg_color': (255, 255, 255)})
            file_txtbox.text = level._filename

            load_bttn.attach(file_txtbox)
            save_bttn.attach(file_txtbox)
            self.focus(file_txtbox)
        except (IndexError, ValueError, TypeError, KeyError):
            print('Error during creation of GuiLevelOptions')

    def destroy(self, *args):
        GuiState.destroy(self)
        self.controls[:] = []