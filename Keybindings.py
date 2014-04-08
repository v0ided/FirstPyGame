__author__ = 'thvoidedline'
from Timer import Timer
from Binding import Binding


class Keybindings():
    _delay_timer = None
    _is_delay = False

    def __init__(self):
        self._bindings = []
        Keybindings._delay_timer = Timer(300, Keybindings._fin_delay)

    def __getitem__(self, item):
        try:
            return self._bindings[item]
        except IndexError:
            print('Invalid keybinding index')
            return None

    @staticmethod
    def _start_delay():
        Keybindings._is_delay = True
        Keybindings._delay_timer.start_timer()

    @staticmethod
    def _fin_delay():
        Keybindings._is_delay = False
        if Keybindings._delay_timer:
            Keybindings._delay_timer.stop_timer()

    def check(self, key):
        if self._is_delay:
            pass
        else:
            for bind in self._bindings:
                if bind.enable:
                    if key == bind.key():
                        bind.function()
                        Keybindings._start_delay()
                        return True
        return False

    def add(self, binding):
        if binding:
            if isinstance(binding, Binding):
                self._bindings.append(binding)

    def remove(self, key):
        for bind in self._bindings:
            if bind.key == key:
                self._bindings.remove(bind)

    #Controls if binding will execute function on keypress
    #binding_type = the subclass type for the bind you want to toggle state of
    #  This works because every binding has its own subclass, which allows other keybindings to toggle inappropriate or
    #  conflicting bindings without specifying a specific key or having a reference to the instance
    def toggle(self, binding_type, on=None):
        for bind in self._bindings:
            if isinstance(bind, binding_type):
                if on is None:
                    if bind.enable is True:
                        bind.enable = False
                    else:
                        bind.enable = True
                else:
                    if isinstance(on, bool):
                        bind.enable = on
                    else:
                        print('Invalid state. State must be boolean.')