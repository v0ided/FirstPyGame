import pygame
from Constants import *


class Binding():
    def __init__(self, key, *args):
        self._key = key
        self.args = []
        for arg in args:
            self.args.append(arg)
        self.enable = True

    def key(self):
        return self._key

    #overload this
    def function(self):
        pass


class ListboxUpBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            obj_name, gui_state = self.args
            gui_state.get_obj(obj_name).select_next(DIR_UP)


class ListboxDownBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            obj_name, gui_state = self.args
            gui_state.get_obj(obj_name).select_next(DIR_DOWN)


class ButtonEnter(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            bttn = self.args[0]
            #simulate a button press
            bttn.key_input(pygame.MOUSEBUTTONUP)


class SelectNextTxtboxBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            gui_state = self.args[0]
            gui_state.focus_next_control(TXT_BOX)