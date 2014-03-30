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
            level.save_level()


class LevelLoadBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            level = self.args[0]
            level.load_level()


class LevelClearBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            level = self.args[0]
            level.clear_level()


class PrePlaceObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            obj_name, obj_search_gui, level, sel_obj_gui = self.args
            level.pre_place_object(obj_search_gui.get_obj(obj_name).get_text())
            obj_search_gui.toggle_active(False)
            sel_obj_gui.keybindings.toggle(PlaceObjectBind, True)


class PlaceObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            level, obj_search_gui = self.args
            level.place_object()


class ToggleSearchBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            obj_search_gui, sel_obj_gui = self.args
            if obj_search_gui._has_focus:
                print(obj_search_gui._has_focus)
                obj_search_gui.toggle_active(False)
            else:
                obj_search_gui.toggle_active(True)
                sel_obj_gui.keybindings.toggle(PlaceObjectBind, False)

                textbox = obj_search_gui.get_obj("c_obj")
                listbox = obj_search_gui.get_obj("results")
                mouse_pos = pygame.mouse.get_pos()

                obj_search_gui._has_focus = textbox
                textbox.cords = mouse_pos
                listbox.cords = (textbox.cords[X], textbox.cords[Y] + textbox.h + 25)


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
