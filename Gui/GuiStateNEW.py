__author__ = 'thvoidedline'

from Gui.GuiObjectFactory import GuiObjFactory
from Keybindings import Keybindings
from Constants import *


class GuiState():
    def __init__(self, state, *args):
        #List of all gui objects the state controls
        self.controls = []
        #keyboard character/function to execute
        self.keybindings = Keybindings()
        #Object in self.objects that has the current focus for input
        self._has_focus = None
        #Index of focus object in objects
        self._focus_index = 0
        #Toggle display of objects and action of keybindings for state
        self.state = state
        #Is state active?
        self._active = False
        #Toggle visibility of gui objects, keybindings will still be active if False
        self.visible = True
        #args is any needed outside data
        self.create(*args)

    #Set any data that needs to be reset or is only wanted when the state is active (such as keybindings)
    def create(self, *args):
        self._active = True

    #Delete any data that needs to be reset or is only wanted when the state is active (such as keybindings)
    def destroy(self):
        self._active = False

    def toggle(self, *args):
        if self._active:
            self.destroy()
        else:
            self.create(*args)

    def add(self, obj_type, var_dict):
        self.controls.append(GuiObjFactory(obj_type, var_dict))
        return self.controls[-1]

    def remove(self, obj):
        if obj in self.controls:
            self.controls.remove(obj)

    def draw(self, screen):
        if self.visible:
            for obj in self.controls:
                if obj.visible:
                    obj.draw(screen)

    def update(self):
        for obj in self.controls:
            obj.update()

    def get_obj(self, name):
        for obj in self.controls:
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
                #self.toggle_active()
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
            self._focus_index = self.controls.index(obj)
            self._has_focus.is_focus = True

    def get_focus(self):
        return self._has_focus

    def object_text(self, name):
        obj = self.get_obj(name)
        if obj:
            return obj.get_text()
        print('Object not found.')
        return ""

    def change_state(self, state):
        self.state = state

    #check if a gui object is at a SCREEN coordinate, call input if object is at x,y
    def click_gui_objects_at(self, x, y):
        clicked = False
        for gobj in self.controls:
            if gobj.rect.collidepoint(x, y):
                gobj.input(pygame.MOUSEBUTTONUP)
                clicked = True
        return clicked

    def focus_next_control(self, filter_type):
        if self._focus_index < len(self.controls) - 1:
            self._focus_index += 1
        else:
            self._focus_index = 0

        if self.controls[self._focus_index].type != filter_type:
            self.focus_next_control(filter_type)

        self.focus(self.controls[self._focus_index])
        print(str(self._focus_index))