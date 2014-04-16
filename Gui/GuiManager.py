

class GuiManager():
    def __init__(self):
        self.states = {}

    #Returns true if a gui object was clicked, False if not
    #Handles key input by passing it to state obj to check if has_focus gui object exists to give input to
    def input(self, user_input):
        clicked_obj = False
        for state_type, state_obj in self.states.items():
            #state input function is responsible for checking if it is ok to process input
            clicked_obj = state_obj.input(user_input)
        return clicked_obj

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