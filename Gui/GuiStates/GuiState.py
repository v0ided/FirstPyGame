__author__ = 'thvoidedline'

import pygame
from Gui.GuiObjectFactory import GuiObjFactory
from Keybindings import Keybindings
from Constants import BUTTON
from Binding import Binding


class GuiState():
    def __init__(self, is_blocking):
        #List of all gui objects the state controls
        self.controls = []
        #keyboard character/function to execute
        self.keybindings = Keybindings()
        #Object in self.objects that has the current focus for input
        self._has_focus = None
        #Index of focus object in objects
        self._focus_index = 0
        #Toggle display of objects and action of keybindings for state
        self.blocking = is_blocking
        #Is state active?
        self._active = False
        #Toggle visibility of gui objects, keybindings will still be active if False
        self.visible = True

    #Set any data that needs to be reset or is only wanted when the state is active (such as keybindings)
    def create(self, *args):
        print('GuiState parent create called')
        self._active = True
        self.keybindings.add(EscExitBind(pygame.K_ESCAPE, self))

    #Delete any data that needs to be reset or is only wanted when the state is active (such as keybindings)
    def destroy(self):
        print('GuiState parent destroy called')
        self.focus(None)
        self._active = False
        self.keybindings.remove(pygame.K_ESCAPE)

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

    def _mouse_input(self, m_input):
        if m_input == pygame.MOUSEBUTTONUP:
            m_x, m_y = pygame.mouse.get_pos()
            clicked_obj = self.click_gui_objects_at(m_x, m_y)
            if clicked_obj is None:
                print('clicked nothing at ' + str(len(self.controls)))
                self.focus(None)
                return False
            else:
                print('clicked gui object' + str(clicked_obj.type))
                self.focus(clicked_obj)
                if clicked_obj.type == BUTTON:
                    if clicked_obj.close_state:
                        self.destroy()
                return True

    def input(self, user_input):
        if user_input == pygame.MOUSEBUTTONUP:
            return self._mouse_input(user_input)

        #If a key binding exists, do action
        if self.keybindings.check(user_input):
            return True

        #if a state object has focus, give input to object
        if self._has_focus:
            #Only send alphanumeric characters and backspace to state for input
            if pygame.K_ESCAPE < user_input < pygame.K_DELETE or user_input == pygame.K_BACKSPACE:
                print('input sent to focused gui object')
                self._has_focus.input(user_input)
                return True

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

    def get_focus_obj(self):
        return self._has_focus

    def object_text(self, name):
        obj = self.get_obj(name)
        if obj:
            return obj.get_text()
        print('Object not found.')
        return ""

    #check if a gui object is at a SCREEN coordinate, call input if object is at x,y
    #returns type of gui object clicked
    def click_gui_objects_at(self, x, y):
        clicked = None
        for gobj in self.controls:
            if gobj.rect.collidepoint(x, y):
                gobj.input(pygame.MOUSEBUTTONUP)
                clicked = gobj
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


class EscExitBind(Binding):
    def __init__(self, key, *args):
        Binding.__init__(self, key, *args)

    def function(self):
        try:
            self.args[0].destroy()
        except KeyError:
            print('invalid state sent to EscExitBind')
            raise