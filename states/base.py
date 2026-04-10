class StateBase:
    def __init__(self, engine):
        self.engine = engine

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass
