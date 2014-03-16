__author__ = 'thvoidedline'


from Constants import *
from Textbox import Textbox
from Listbox import Listbox


class GuiManager():
    def __init__(self):
        self.objects = []
        self.active_input = None

    def factory(self, obj_type, name, cords, var_dict):
        if obj_type == TXT_BOX:
            self.objects.append(Textbox(name, cords))
            self.active_input = self.objects[-1]
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

    def display(self, screen):
        for obj in self.objects:
            obj.display(screen)

    def keyboard_input(self, key):
        if self.active_input:
            if self.active_input.type == TXT_BOX:
                self.active_input.get(key)

    def update(self):
        for obj in self.objects:
            obj.update()

    def remove(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def get_obj(self, name):
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None