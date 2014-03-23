__author__ = 'thvoidedline'

import pygame
from Constants import *
from Textbox import Textbox
from Listbox import Listbox


class GuiManager():
    def __init__(self):
        #List of all gui objects the manager controls
        self.objects = []
        #keyboard character/function to execute
        self.bindings = {}
        #mouse button/function to execute
        self.mouse_bindings = {}
        #Object in self.objects that has the current focus for input
        self.__has_focus = None

    def add(self, obj_type, name, cords, var_dict):
        if obj_type == TXT_BOX:
            self.objects.append(Textbox(name, cords))
            self.__has_focus = self.objects[-1]
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

    def display(self, screen):
        for obj in self.objects:
            if obj.visible:
                obj.display(screen)

    def update(self):
        for obj in self.objects:
            obj.update()

    def get_obj(self, name):
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None

    def input(self, key):
        #If a key binding exists, does action then returns
        if self.check_binding(key):
            return
        if self.__has_focus:
            if self.__has_focus.type == TXT_BOX:
                self.__has_focus.get(key)

    def bind(self, function, pressed):
        if function and pressed:
            if pressed in self.bindings.keys():
                print("Overwriting key binding: " + str(pressed))
            self.bindings[pressed] = function
        else:
            print('Function or key invalid in bind call.')

    def unbind(self, key):
        if key in self.bindings.keys():
            del self.bindings[key]

    def check_binding(self, key):
        if key in self.bindings.keys():
            self.bindings.get(key)()
            return True
        return False

    def check_mouse_binding(self, event_type):
        if event_type in self.mouse_bindings.keys():
            self.mouse_bindings.get(event_type)()
            return True
        return False

    def tog_obj_search(self):
        if self.__has_focus:
                self.remove(self.__has_focus)
                self.remove(self.get_obj('results'))
                self.__has_focus = None
                self.unbind(pygame.K_TAB)
        else:
            #Create a text box and add a listbox to display filtered results
            if self.get_obj("c_obj"):
                self.get_obj("c_obj").visible = True
                self.get_obj("results").visible = True
            else:
                txt_box = self.add(TXT_BOX, "c_obj", pygame.mouse.get_pos(), None)
                results_pos = (txt_box.cords[X], txt_box.cords[Y] + txt_box.h + 45)
                results = self.add(LIST_BOX, "results", results_pos, None)
                self.bind(results.select_next, pygame.K_TAB)
                txt_box.attach(results)

    def get_focus(self):
        return self.__has_focus

    def object_text(self, name):
        obj = self.get_obj(name)
        if obj:
            return obj.get_text()
        print('Object not found.')
        return ""