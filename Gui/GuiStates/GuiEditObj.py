from Gui.GuiStates.GuiState import GuiState

__author__ = 'thvoidedline'

from Binding import SelectNextTxtboxBind
from Constants import *
from HelpFunctions import obj_type_str


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

            self.add(WINDOW, {'name': 'editprops', 'cords': (300, 250), 'w': 250, 'h': 330,
                              'bg_color': (0, 0, 0), 'font_color': (234, 234, 234)})
            confirm_bttn = self.add(BUTTON, {'name': 'confirm_bttn', 'cords': (320, 535),
                                             'bg_color': (255, 255, 255), 'font_color': (0, 0, 0),
                                             'font_size': 14, 'text': 'Confirm',
                                             'action': level.edit_object, 'close_state': True})

            self.add(TEXT, {'name': 'namelabel', 'cords': (310, 280), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Name:"})
            namefield = self.add(TXT_BOX, {'name': 'nametxtbox', 'cords': (400, 284), 'bg_color': (255, 255, 255)})
            namefield.text = obj.name
            confirm_bttn.attach('name', namefield)

            self.add(TEXT, {'name': 'xlabel', 'cords': (310, 305), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "X:"})
            xfield = self.add(TXT_BOX, {'name': 'xtxtbox', 'cords': (400, 305), 'bg_color': (255, 255, 255)})
            xfield.text = str(obj.rect.x)
            confirm_bttn.attach('x', xfield)

            self.add(TEXT, {'name': 'ylabel', 'cords': (310, 330), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Y:"})
            yfield = self.add(TXT_BOX, {'name': 'ytxtbox', 'cords': (400, 330), 'bg_color': (255, 255, 255)})
            yfield.text = str(obj.rect.y)
            confirm_bttn.attach('y', yfield)

            self.add(TEXT, {'name': 'wlabel', 'cords': (310, 355), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Width:"})
            wfield = self.add(TXT_BOX, {'name': 'wtxtbox', 'cords': (400, 355), 'bg_color': (255, 255, 255)})
            wfield.text = str(obj.rect.w)
            confirm_bttn.attach('w', wfield)

            self.add(TEXT, {'name': 'hlabel', 'cords': (310, 380), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Height:"})
            hfield = self.add(TXT_BOX, {'name': 'htxtbox', 'cords': (400, 380), 'bg_color': (255, 255, 255)})
            hfield.text = str(obj.rect.h)
            confirm_bttn.attach('h', hfield)

            self.add(TEXT, {'name': 'glabel', 'cords': (310, 405), 'font_color': (234, 234, 234),
                                              'font_size': 18, 'text': "Gravity:"})
            gravityfield = self.add(TXT_BOX, {'name': 'gtxtbox', 'cords': (400, 405), 'bg_color': (255, 255, 255)})
            gravityfield.text = str(obj.obey_gravity)
            confirm_bttn.attach('gravity', gravityfield)

            self.add(TEXT, {'name': 'clabel', 'cords': (310, 430), 'font_color': (234, 234, 234),
                                              'font_size': 18, 'text': "Collidable:"})
            collidefield = self.add(TXT_BOX, {'name': 'ctxtbox', 'cords': (400, 430), 'bg_color': (255, 255, 255)})
            collidefield.text = str(obj.collidable)
            confirm_bttn.attach('collide', collidefield)

            self.add(TEXT, {'name': 'layerlabel', 'cords': (310, 455), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Layer:"})
            layerfield = self.add(TXT_BOX, {'name': 'layertxtbox', 'cords': (400, 455), 'bg_color': (255, 255, 255)})
            layerfield.text = str(obj._layer)
            confirm_bttn.attach('layer', layerfield)

            self.add(TEXT, {'name': 'typelabel', 'cords': (310, 480), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "Type:"})
            typefield = self.add(TXT_BOX, {'name': 'typetxtbox', 'cords': (400, 480), 'bg_color': (255, 255, 255)})
            typefield.text = obj_type_str(obj.type)
            confirm_bttn.attach('type', typefield)

            self.add(TEXT, {'name': 'filelabel', 'cords': (310, 505), 'font_color': (234, 234, 234),
                            'font_size': 18, 'text': "File:"})
            filefield = self.add(TXT_BOX, {'name': 'filetxtbox', 'cords': (400, 505), 'bg_color': (255, 255, 255)})
            filefield.text = obj.files[0]
            confirm_bttn.attach('file1', filefield)

        except (ValueError, IndexError, LookupError, TypeError):
            print('Error during creation of GuiEditObject')
            raise

    def destroy(self):
        print('GuiEditObj destroy called')
        GuiState.destroy(self)
        self.keybindings.remove(pygame.K_TAB)
        self.controls[:] = []