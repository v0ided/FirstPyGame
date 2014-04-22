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


class LevelSaveBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            level = self.args[0]
            level.new_save()


class LevelLoadBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            load_lvl_dialog = self.args[0]
            load_lvl_dialog.toggle_active()
            if load_lvl_dialog.is_active():
                load_lvl_dialog.focus(load_lvl_dialog.get_obj('file_txtbox'))


class LevelSaveAsBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            save_lvl_gui = self.args[0]
            save_lvl_gui.toggle_active()
            if save_lvl_gui.is_active():
                save_lvl_gui.focus(save_lvl_gui.get_obj('saveas_txtbox'))


class LevelClearBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            clear_lvl_gui = self.args[0]
            clear_lvl_gui.toggle_active()


class ToggleStateBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        self.args[0].toggle()


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
            bttn.input(pygame.MOUSEBUTTONUP)


class DeleteObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            level = self.args[0]
            level.remove_object(level.selected_obj)
            level.selected_obj = None


class SelectNextTxtboxBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            gui_state = self.args[0]
            gui_state.focus_next_control(TXT_BOX)