

class GuiManager():
    def __init__(self):
        self.states = {}
        self.active_blocking = False

    #Returns true if a gui state was clicked, False if not
    #Passes user input first blocking state or first successful non-blocking state
    def input(self, user_input):
        blocking = (next((state for state in self.states.values()
                          if state.blocking is True and state._active is True), None))

        if blocking:
            print('Blocking menu found, sending input')
            return blocking.input(user_input)
        else:
            avail_input = False
            for state_type, state_obj in self.states.items():
                #state input function is responsible for checking if it is ok to process input
                avail_input = state_obj.input(user_input)
                #If a positive input is found, don't check the rest of the states
                if avail_input:
                    break
            return avail_input

    def update(self):
        for state_type, state_obj in self.states.items():
            state_obj.update()
        self.check_still_blocking()

    def add(self, state, state_obj):
        if state in self.states.keys():
            print('Overwriting gui state.')
        self.states[state] = state_obj

    def toggle_state(self, state_type, *args):
        if state_type in self.states.keys():
            state = self.states[state_type]
            self.active_blocking = state.blocking
            if state._active:
                state.destroy()
            else:
                state.create(*args)
        else:
            print('Gui state does not exist.')

    def check_still_blocking(self):
        for state in self.states.values():
            if state.blocking:
                if state._active:
                    #Should not be needed, but will fix blocking if state is toggled outside of manager function
                    self.active_blocking = True
                    return
        self.active_blocking = False

    def draw(self, screen):
        for state_type, state_obj in self.states.items():
            state_obj.draw(screen)