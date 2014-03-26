__author__ = 'thvoidedline'

import pygame
from Constants import *
from Textbox import Textbox
from Listbox import Listbox


class GuiState():
    def __init__(self, active=True):
        #List of all gui objects the manager controls
        self.objects = []
        #keyboard character/function to execute
        self.bindings = {}
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
        if self.check_binding(key):
            return
        #if focus object
        if self._has_focus:
            self._has_focus.input(key)

    def bind(self, get_args, function, pressed):
        if function and pressed:
            if pressed in self.bindings.keys():
                print("Overwriting key binding: " + str(pressed))
            self.bindings[pressed] = (get_args, function)
        else:
            print('Function or get_args or key invalid in bind call.')

    def unbind(self, key):
        if key in self.bindings.keys():
            del self.bindings[key]

    def check_binding(self, key):
        if key in self.bindings.keys():
            args = None
            if self.bindings.get(key)[0]:
                args = self.bindings.get(key)[0]()
            self.bindings[key][1](args)
            return True
        return False

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


class ObjSearchGui(GuiState):
    def __init__(self, active=True):
        GuiState.__init__(self, active)

    def get_file_from_input(self):
        if self.get_obj("results"):
            return self.get_obj("results").get_text()
        else:
            print("no results text box found")
            return ""

    def tog_obj_search(self, arg):
        if self._has_focus:
                self.remove(self._has_focus)
                self.remove(self.get_obj('results'))
                self._has_focus = None
                self.visible = False
        else:
            self.visible = True
            self._has_focus = self.get_obj("c_obj")
            #Create a text box and add a listbox to display filtered results
            txt_box = self.add(TXT_BOX, "c_obj", pygame.mouse.get_pos(), None)
            results_pos = (txt_box.cords[X], txt_box.cords[Y] + txt_box.h + 45)
            results = self.add(LIST_BOX, "results", results_pos, None)
            txt_box.attach(results)