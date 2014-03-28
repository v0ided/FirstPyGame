__author__ = 'thvoidedline'

from Binding import Binding


class Keybindings():
    def __init__(self):
        self._bindings = []

    def __getitem__(self, item):
        try:
            return self._bindings[item]
        except IndexError:
            print('Invalid keybinding index')
            return None

    def check(self, key):
        for bind in self._bindings:
            if key == bind.key():
                bind.function()

    def add(self, binding):
        if binding:
            if isinstance(binding, Binding):
                self._bindings.append(binding)

    def remove(self, binding):
        if binding in self._bindings:
            self._bindings.remove(binding)

    #Controls if binding will execute function on keypress
    def toggle(self, binding, state=None):
        if binding in self._bindings:
            if state is None:
                if self._bindings.enable is True:
                    self._bindings.enable = False
                else:
                    self._bindings.enable = True
            else:
                if isinstance(state, bool):
                    self._bindings.enable = state
                else:
                    print('Invalid state. State must be boolean.')