"""
Contains implementation of state machine with required utils.
"""

from typing import Callable
from .exceptions import StateNotFoundError, CurrentStateNotDefinedError
from .utils import log_state_machine_states


class State:
    """Creates state with required callbacks."""

    def __init__(self, name: str, run_callback: Callable, on_update_callback: Callable) -> None:
        self.name = name
        self.run_callback = run_callback
        self.on_update_callback = on_update_callback

    def run(self) -> None:
        """Runs main state logic."""

        self.run_callback()

    def update(self) -> None:
        """Runs transition logic."""

        self.on_update_callback()


class StateMachine:
    """Creates state machine."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.current_state = None
        self.states = {}
        self.context = {}
        self.is_active = False

    def add_state(self, state: State) -> None:
        """
        Adds single state to state machine.

        :param state: state to add
        :return: None
        """

        self.states[state.name.lower()] = state

    def go_to_state(self, state_name: str) -> None:
        """
        Jumps to specified state.

        :param state_name: name of next state
        :return: None
        """

        state = self.states.get(state_name.lower())

        if state is None:
            log_state_machine_states(self)
            raise StateNotFoundError(
                'State "{}" was not added to "{}" state machine.'.format(state_name, self.name))

        self.current_state = state
        self.current_state.run()

    def update(self) -> None:
        """
        Goes to next state.

        :return: None
        """

        if self.current_state is None:
            raise CurrentStateNotDefinedError('State machine is not in any of the states. '
                                              'Call keyword "Go To State..." or "Run State Machine ...start_from=..." '
                                              'keywords to enter the state.')

        self.current_state.update()

    def activate(self) -> None:
        """
        Sets state machine in active state.

        :return: None
        """

        self.is_active = True

    def deactivate(self) -> None:
        """
        Sets state machine in deactivated state.

        :return: None
        """

        self.is_active = False
