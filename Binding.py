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
            level.save()


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


class LevelQuitBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            quit_lvl_gui = self.args[0]
            quit_lvl_gui.toggle_active()
            #If after toggling the state isn't active - the user pressed Esc twice, exit game
            if not quit_lvl_gui.is_active():
                pygame.event.post(pygame.event.Event(QUIT_EVENT))


class PrePlaceObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        try:
            obj_search, level = self.args
            obj_search.pre_place_obj(level)
        except IndexError:
            print('Error - Invalid arguments passed to PrePlaceObjectBind')


#todo: Needed? What is the difference between this and selectObjectBind
class PlaceSearchObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            level, obj_search_gui = self.args
            saveas_txtbox = obj_search_gui.get_obj("saveas_txtbox")
            if saveas_txtbox:
                level.place_object()


class ToggleStateBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        try:
            self.args[0].toggle()
        except IndexError:
            print('Error - Did you forget to pass GuiState to ToggleStateBind?')


class GuiEditObjBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            gui_state, level = self.args
            if level.selected_obj is None:
                print('Tried to edit NoneType Object')
            else:
                if gui_state.is_active():
                    print("Gui State is active, toggling?")
                    #deselect any controls selected from last time
                    gui_state.focus(None)
                    #give movement control of selected object back to user
                    level.focus_menu(False)
                else:
                    #fill textboxes with object data
                    gui_state.get_obj('nametxtbox').str_input(level.selected_obj.name, True)
                    gui_state.get_obj('xtxtbox').str_input(str(level.selected_obj.rect.x), True)
                    gui_state.get_obj('ytxtbox').str_input(str(level.selected_obj.rect.y), True)
                    gui_state.get_obj('wtxtbox').str_input(str(level.selected_obj.rect.w), True)
                    gui_state.get_obj('htxtbox').str_input(str(level.selected_obj.rect.h), True)
                    gui_state.get_obj('gravitytxtbox').str_input(str(level.selected_obj.obey_gravity), True)
                    gui_state.get_obj('collidetxtbox').str_input(str(level.selected_obj.collidable), True)
                    gui_state.get_obj('layertxtbox').str_input(str(level.selected_obj._layer), True)
                    #tell the level to not move selected object until focus_menu is False
                    level.focus_menu(True)


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


class SelectObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            level = self.args[0]
            level.input(pygame.MOUSEBUTTONUP)


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