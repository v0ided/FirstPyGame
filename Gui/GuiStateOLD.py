__author__ = 'thvoidedline'

from Gui.GuiObjectFactory import GuiObjFactory
from Keybindings import Keybindings
from Constants import *


class GuiStateOLD():
    def __init__(self, active=True):
        #List of all gui objects the manager controls
        self.objects = []
        #keyboard character/function to execute
        self.keybindings = Keybindings()
        #toggle state._active keybind, if one is desired
        self.toggle_bind = None
        #mouse button/function to execute
        self.mouse_bindings = {}
        #Object in self.objects that has the current focus for input
        self._has_focus = None
        #Index of focus object in objects
        self._focus_index = 0
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
        #if focus object
        if self._has_focus:
            self._has_focus.input(user_input)

        if self.toggle_bind:
            if self.toggle_bind.key() == user_input:
                #do initializing, if any
                self.toggle_bind.function()
                self.toggle_active()
                return True

        if self._active:
            #If a key binding exists, do action
            if self.keybindings.check(user_input):
                return True
            if user_input == pygame.MOUSEBUTTONUP:
                m_x, m_y = pygame.mouse.get_pos()
                if self.click_gui_objects_at(m_x, m_y):
                    print('mouse click')
                    return True
                else:
                    self.focus(None)
        return False

    def focus(self, obj):
        #If there is a currently focused object, let it know it is no longer selected
        if self._has_focus:
            self._has_focus.is_focus = False

        self._has_focus = obj

        if self._has_focus is None:
            self._focus_index = -1
        else:
            self._focus_index = self.objects.index(obj)
            self._has_focus.is_focus = True

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
        if state:
            self._active = not state

        if self._active:
            self._active = False
            self._has_focus = None
            self.visible = False
            self.focus(None)
        else:
            self._active = True
            self.visible = True
            self._has_focus = None

    #check if a gui object is at a SCREEN coordinate, call input if object is at x,y
    def click_gui_objects_at(self, x, y):
        clicked = False
        for gobj in self.objects:
            if gobj.rect.collidepoint(x, y):
                gobj.input(pygame.MOUSEBUTTONUP)
                clicked = True
        return clicked

    def select_next_control(self, filter_type):
        if self._focus_index < len(self.objects) - 1:
            self._focus_index += 1
        else:
            self._focus_index = 0

        if self.objects[self._focus_index].type != filter_type:
            self.select_next_control(filter_type)

        self.focus(self.objects[self._focus_index])
        print(str(self._focus_index))