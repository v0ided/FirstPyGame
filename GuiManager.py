

class GuiManager():
    def __init__(self):
        self.states = {}

    def input(self, key):
        for state_type, state_obj in self.states.items():
            if state_obj.is_active():
                state_obj.input(key)

    def update(self):
        for state_type, state_obj in self.states.items():
            if state_obj.is_active():
                state_obj.update()

    def add(self, state, state_obj):
        if state in self.states.keys():
            print('Overwriting gui state.')
        self.states[state] = state_obj

    def activate(self, state):
        if state in self.states.keys():
            self.states[state].toggle_active(True)
        else:
            print('Gui state does not exist.')

    def deactivate(self, state):
        if state in self.states.keys():
            self.states[state].toggle_active(False)
        else:
            print('Gui state does not exist.')

    def draw(self, screen):
        for state_type, state_obj in self.states.items():
            if state_obj.is_active():
                state_obj.draw(screen)