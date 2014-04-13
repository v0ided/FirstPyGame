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
        if self.args:
            obj_name, obj_search_gui, level, sel_obj_gui = self.args
            level.pre_place_object(obj_search_gui.get_obj(obj_name).get_text())
            obj_search_gui.toggle_active(False)
            sel_obj_gui.keybindings.toggle(PlaceSearchObjectBind, True)


class PlaceSearchObjectBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            level, obj_search_gui = self.args
            saveas_txtbox = obj_search_gui.get_obj("saveas_txtbox")
            if saveas_txtbox:
                level.place_object()


class ToggleSearchBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            obj_search_gui, sel_obj_gui = self.args
            if obj_search_gui.get_focus():
                obj_search_gui.toggle_active(False)
            else:
                obj_search_gui.toggle_active(True)
                sel_obj_gui.keybindings.toggle(PlaceSearchObjectBind, False)

                textbox = obj_search_gui.get_obj("c_obj")
                listbox = obj_search_gui.get_obj("results")
                assert listbox, "results does not exist"
                assert textbox, "c_obj does not exist"

                mouse_pos = pygame.mouse.get_pos()

                obj_search_gui.focus(textbox)
                textbox.rect.x, textbox.rect.y = mouse_pos
                listbox.rect.x = textbox.rect.x
                listbox.rect.y = textbox.rect.y + textbox.rect.h + 25


class GuiEditObjBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        if self.args:
            gui_state, level, select_gui = self.args
            obj = level.selected_obj
            if obj:
                if gui_state.is_active():
                    pass
                else:
                    gui_state.get_obj('nametxtbox').text = obj.name
                    gui_state.get_obj('xtxtbox').text = str(obj.rect.x)
                    gui_state.get_obj('ytxtbox').text = str(obj.rect.y)
                    gui_state.get_obj('wtxtbox').text = str(obj.rect.w)
                    gui_state.get_obj('htxtbox').text = str(obj.rect.h)
                    gui_state.get_obj('gravitytxtbox').text = str(obj.obey_gravity)
                    gui_state.get_obj('collidetxtbox').text = str(obj.collidable)
                    gui_state.get_obj('layertxtbox').text = str(obj._layer)

                    level.focus_menu(True)
                    select_gui.toggle_active()


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
            gui_state.select_next_control(TXT_BOX)