

class State(object):
    def __init__(self, name, run_callback, on_update_callback):
        self.name = name
        self.run_callback = run_callback
        self.on_update_callback = on_update_callback

    def run(self):
        self.run_callback()

    def update(self):
        self.on_update_callback()


class Context(dict):
    pass


class StateMachine(object):
    def __init__(self, name: str) -> None:
        self.current_state = None
        self.states = {}
        self.context = Context()

    def add_state(self, state: State):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        self.current_state = self.states[state_name]
        self.current_state.run()

    def update(self):
        if self.current_state is not None:
            self.current_state.update()
