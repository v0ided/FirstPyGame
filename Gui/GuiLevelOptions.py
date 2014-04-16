__author__ = 'thvoidedline'

from Gui.GuiStateNEW import GuiState
from Constants import *


class GuiLevelOptions(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state, *args)
        self.create(*args)

    def create(self, *args):
        GuiState.create(self, *args)
        try:
            level = args[0]
            self.add(WINDOW, {'name': "leveloptions", 'cords': (0, 560), 'w': 200, 'h': 160,
                                            'bg_color': (0, 0, 0), 'font_color': (234, 234, 234)})
            self.add(TEXT, {'name': "keymap", 'cords': (5, 565), 'font_color': (234, 234, 234), 'font_size': 20,
                            'text': "Save Level - F1 Load Level - F2 Clear Level - F3 | Level: ",
                            'watch': level.get_filename})
            self.add(BUTTON, {'name': 'clear_bttn', 'cords': (320, 450), 'bg_color': (255, 255, 255),
                                                'font_color': (0, 0, 0), 'font_size': 14,
                                                'text': 'Clear Level', 'action': level.clear_level})
            self.add(BUTTON, {'name': 'load_bttn', 'cords': (320, 490), 'bg_color': (255, 255, 255),
                                               'font_color': (0, 0, 0), 'font_size': 14,
                                               'text': 'Clear Level', 'action': level.load})
            save_txtbox = self.add(TXT_BOX, {'name': 'saveas_txtbox', 'cords': (320, 510), 'bg_color': (255, 255, 255)})
            save_txtbox.text = level._filename
            save_bttn = self.add(BUTTON, {'name': 'save_bttn', 'cords': (400, 510), 'bg_color': (255, 255, 255),
                                               'font_color': (0, 0, 0), 'font_size': 14,
                                               'text': 'Clear Level', 'action': level.save})
            save_bttn.attach(save_txtbox)
            self.focus(save_txtbox)
        except (IndexError, ValueError, TypeError):
            print('Error during creation of GuiLevelOptions')

    def destroy(self):
        GuiState.destroy(self)
        del self.controls[:]

