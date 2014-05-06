from Gui.GuiStates.GuiState import GuiState

__author__ = 'thvoidedline'

from Binding import SelectNextTxtboxBind
from Constants import *


class GuiEditObj(GuiState):
    def __init__(self, state, *args):
        GuiState.__init__(self, state, *args)

    def create(self, *args):
        GuiState.create(self, *args)
        try:
            level = args[0]
            obj = args[1]
            if obj is None:
                print('none obj')
                return

            self.keybindings.add(SelectNextTxtboxBind(pygame.K_TAB, self))

            self.add(WINDOW, {'name': 'editprops', 'cords': (300, 250), 'w': 250, 'h': 260,
                              'bg_color': (0, 0, 0), 'font_color': (234, 234, 234)})
            confirm_bttn = self.add(BUTTON, {'name': 'confirm_bttn', 'cords': (320, 480),
                                             'bg_color': (255, 255, 255), 'font_color': (0, 0, 0),
                                             'font_size': 14, 'text': 'Confirm',
                                             'action': level.edit_object, 'close_state': True})

            self.add(TEXT, {'name': 'namelabel', 'cords': (310, 280), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Name:"})
            namefield = self.add(TXT_BOX, {'name': 'nametxtbox', 'cords': (400, 284), 'bg_color': (255, 255, 255)})
            namefield.text = obj.name
            confirm_bttn.attach(namefield)

            self.add(TEXT, {'name': 'xlabel', 'cords': (310, 305), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "X:"})
            xfield = self.add(TXT_BOX, {'name': 'xtxtbox', 'cords': (400, 305), 'bg_color': (255, 255, 255)})
            xfield.text = str(obj.rect.x)
            confirm_bttn.attach(xfield)

            self.add(TEXT, {'name': 'ylabel', 'cords': (310, 330), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Y:"})
            yfield = self.add(TXT_BOX, {'name': 'ytxtbox', 'cords': (400, 330), 'bg_color': (255, 255, 255)})
            yfield.text = str(obj.rect.y)
            confirm_bttn.attach(yfield)

            self.add(TEXT, {'name': 'wlabel', 'cords': (310, 355), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Width:"})
            wfield = self.add(TXT_BOX, {'name': 'wtxtbox', 'cords': (400, 355), 'bg_color': (255, 255, 255)})
            wfield.text = str(obj.rect.w)
            confirm_bttn.attach(wfield)

            self.add(TEXT, {'name': 'hlabel', 'cords': (310, 380), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Height:"})
            hfield = self.add(TXT_BOX, {'name': 'htxtbox', 'cords': (400, 380), 'bg_color': (255, 255, 255)})
            hfield.text = str(obj.rect.h)
            confirm_bttn.attach(hfield)

            self.add(TEXT, {'name': 'glabel', 'cords': (310, 405), 'font_color': (234, 234, 234),
                                              'font_size': 18, 'text': "Gravity:"})
            gravityfield = self.add(TXT_BOX, {'name': 'gtxtbox', 'cords': (400, 405), 'bg_color': (255, 255, 255)})
            gravityfield.text = str(obj.obey_gravity)
            confirm_bttn.attach(gravityfield)

            self.add(TEXT, {'name': 'clabel', 'cords': (310, 430), 'font_color': (234, 234, 234),
                                              'font_size': 18, 'text': "Collidable:"})
            collidefield = self.add(TXT_BOX, {'name': 'ctxtbox', 'cords': (400, 430), 'bg_color': (255, 255, 255)})
            collidefield.text = str(obj.collidable)
            confirm_bttn.attach(collidefield)

            self.add(TEXT, {'name': 'layerlabel', 'cords': (310, 455), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Layer:"})
            layerfield = self.add(TXT_BOX, {'name': 'layertxtbox', 'cords': (400, 455), 'bg_color': (255, 255, 255)})
            layerfield.text = str(obj._layer)
            confirm_bttn.attach(layerfield)

        except (ValueError, IndexError, LookupError, TypeError):
            print('Error during creation of GuiEditObject')
            raise

    def destroy(self):
        print('GuiEditObj destroy called')
        GuiState.destroy(self)
        self.keybindings.remove(pygame.K_TAB)
        self.controls[:] = []