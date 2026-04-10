class StateMachine:
    def __init__(self):
        self.states = {}
        self.current_state_name = None
        self.current_state = None

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, name):
        if self.current_state:
            self.current_state.exit()
        
        if name in self.states:
            self.current_state_name = name
            self.current_state = self.states[name]
            self.current_state.enter()
        else:
            self.current_state = None
            self.current_state_name = None

    def handle_events(self, events):
        if self.current_state:
            self.current_state.handle_events(events)

    def update(self):
        if self.current_state:
            self.current_state.update()

    def draw(self, surface):
        if self.current_state:
            self.current_state.draw(surface)
