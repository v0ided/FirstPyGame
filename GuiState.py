__author__ = 'thvoidedline'

import pygame
from Constants import *
from Textbox import Textbox
from Listbox import Listbox
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
        self.active = active
        #Toggle visibility of gui objects, keybindings will still be active if False
        self.visible = True

    def add(self, obj_type, name, cords, var_dict):
        if obj_type == TXT_BOX:
            self.objects.append(Textbox(name, cords))
            self._has_focus = self.objects[-1]
            return self.objects[-1]
        elif obj_type == LIST_BOX:
            item_list = None
            if var_dict:
                if 'items_list' in var_dict:
                    item_list = var_dict['items_list']
            self.objects.append(Listbox(name, cords, item_list))
            return self.objects[-1]
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

    def make_active(self):
        self.active = True