__author__ = 'thvoidedline'

import pygame
from Constants import *
from GuiTextbox import Textbox
from GuiListbox import Listbox
from GuiWindow import GuiWindow
from GuiText import GuiText
from Keybindings import Keybindings


class GuiState():
    def __init__(self, active=True):
        #List of all gui objects the manager controls
        self.objects = []
        #keyboard character/function to execute
        self.keybindings = Keybindings()
        #mouse button/function to execute
        self.mouse_bindings = {}
        #Object in self.objects that has the current focus for input
        self._has_focus = None
        #Toggle display of objects and action of keybindings for state
        self._active = active
        #Toggle visibility of gui objects, keybindings will still be active if False
        self.visible = True

    def add(self, obj_type, name, cords, **kwargs):
        if obj_type == TXT_BOX:
            self.objects.append(Textbox(name, cords))
            return self.objects[-1]
        elif obj_type == LIST_BOX:
            item_list = None
            if kwargs:
                if 'item_list' in kwargs:
                    item_list = kwargs['item_list']
            self.objects.append(Listbox(name, cords, item_list))
            return self.objects[-1]
        elif obj_type == WINDOW:
            if 'w' in kwargs and 'h' in kwargs and 'font_color' in kwargs and 'bg_color' in kwargs:
                w = kwargs['w']
                h = kwargs['h']
                bg_color = kwargs['bg_color']
                font_color = kwargs['font_color']
                self.objects.append(GuiWindow(name, cords, w, h, bg_color, font_color))
            else:
                print("Gui Window was not created - did not have proper arguments")
        elif obj_type == TEXT:
            if 'font_color' in kwargs and 'font_size' in kwargs and 'text' in kwargs:
                font_color = kwargs['font_color']
                font_size = kwargs['font_size']
                text = kwargs['text']
                self.objects.append(GuiText(name, cords, font_color, font_size, text))
            else:
                print("Gui Text was not created - did not have proper arguments")
        else:
            print('Invalid gui object passed to factory.')
        return None

    def remove(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def draw(self, screen):
        if self.visible:
            for obj in self.objects:
                if obj.visible:
                    obj.draw(screen)

    def update(self):
        for obj in self.objects:
            obj.update()

    def get_obj(self, name):
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None

    def input(self, key):
        #If a key binding exists, do action
        if self.keybindings.check(key):
            return
        #if focus object
        if self._has_focus:
            self._has_focus.input(key)

    def check_mouse_binding(self, event_type):
        if event_type in self.mouse_bindings.keys():
            self.mouse_bindings.get(event_type)()
            return True
        return False

    def get_focus(self):
        return self._has_focus

    def object_text(self, name):
        obj = self.get_obj(name)
        if obj:
            return obj.get_text()
        print('Object not found.')
        return ""

    def is_active(self):
        return self._active

    def toggle_active(self, state=None):
        #If state is an argument, set self._active to the opposite of argument and let the toggle code do the work
        if state is not None:
            self._active = not state

        if self._active:
            self._active = False
            self._has_focus = None
            self.visible = False
        else:
            self._active = True
            self.visible = True
            self._has_focus = None