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


#todo: check order of arguments
class PrePlaceObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            gui_state, obj_name, level = self.args
            level.pre_place_object(gui_state.get_obj(obj_name))


class PlaceObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            level = self.args[0]
            level.place_object()


class ToggleSearchBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            gui_state = self.args[0]
            gui_state.make_active()
            if gui_state._has_focus:
                gui_state.remove(gui_state._has_focus)
                gui_state.remove(gui_state.get_obj('results'))
                gui_state._has_focus = None
                gui_state.visible = False
            else:
                gui_state.visible = True
                gui_state._has_focus = gui_state.get_obj("c_obj")
                #Create a text box and add a listbox to display filtered results
                txt_box = gui_state.add(TXT_BOX, "c_obj", pygame.mouse.get_pos(), None)
                results_pos = (txt_box.cords[X], txt_box.cords[Y] + txt_box.h + 45)
                results = gui_state.add(LIST_BOX, "results", results_pos, None)
                txt_box.attach(results)


#todo: fix
class ListboxUpBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            obj_name, gui_state = self.args
            gui_state.get_obj(obj_name).select_next(DIR_UP)


#todo: fix
class ListboxDownBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            obj_name, gui_state = self.args
            gui_state.get_obj(obj_name).select_next(DIR_DOWN)
