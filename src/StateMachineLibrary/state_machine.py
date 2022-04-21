from typing import Callable
from .exceptions import StateNotFoundError
from .utils import log_state_machine_states


class State(object):
    def __init__(self, name: str, run_callback: Callable, on_update_callback: Callable) -> None:
        self.name = name
        self.run_callback = run_callback
        self.on_update_callback = on_update_callback

    def run(self) -> None:
        self.run_callback()

    def update(self) -> None:
        self.on_update_callback()


class StateMachine(object):
    def __init__(self) -> None:
        self.current_state = None
        self.states = {}
        self.context = dict()

    def add_state(self, state: State) -> None:
        self.states[state.name] = state

    def go_to_state(self, state_name: str) -> None:
        if state_name not in self.states:
            log_state_machine_states(self)
            raise StateNotFoundError("State '{}' was not added to state machine.".format(state_name))
        self.current_state = self.states[state_name]
        self.current_state.run()

    def update(self) -> None:
        if self.current_state is not None:
            self.current_state.update()
