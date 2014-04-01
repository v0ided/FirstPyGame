__author__ = 'thvoidedline'

import pygame
from GuiObjectFactory import GuiObjFactory
from Keybindings import Keybindings
from Constants import *


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

    def add(self, obj_type, var_dict):
        self.objects.append(GuiObjFactory(obj_type, var_dict))
        return self.objects[-1]

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

    def input(self, user_input):
        #If a key binding exists, do action
        if self.keybindings.check(user_input):
            return
        #if focus object
        if self._has_focus:
            self._has_focus.input(user_input)
        if user_input == pygame.MOUSEBUTTONUP:
            m_pos = pygame.mouse.get_pos()
            click_obj = self.gui_objects_at(m_pos[X], m_pos[Y])
            if click_obj:
                click_obj.input(user_input)

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

    #check if a gui object is at a SCREEN coordinate
    def gui_objects_at(self, x, y):
        for gobj in self.objects:
            if gobj.rect.collidepoint(x, y):
                return gobj
        return None