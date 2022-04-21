from robot.api import logger

from .store import StateMachineStore
from .state_machine import StateMachine, State
from .utils import is_string, get_keword, build_callback, dict_merge, keyword_should_exist
from .exceptions import StateMachineNotFoundError


class StateMachineFacade(object):
    missing_state_machine_message = "There is no state machine named '{}'. " \
                                    "Call keyword 'Create State Machine' to create it."

    def __init__(self) -> None:
        self._store = StateMachineStore()

    def create_state_machine(self, name: str) -> None:
        if not is_string(name):
            raise RuntimeError('Name of state machine must be a string.')
        if self._store.get(name) is not None:
            logger.warn('State machine named {} has been overwritten'.format(name))
        sm = StateMachine()
        self._store.add(name, sm)

    def add_state(self, state: str, on_update: str, sm: str) -> None:
        sm_instance = self._get_state_machine_or_raise_error(sm)
        keyword_should_exist(state)
        keyword_should_exist(on_update)
        state_keyword = get_keword(state)
        on_update_keyword = get_keword(on_update)
        run_callback = build_callback(state_keyword)
        on_update_callback = build_callback(on_update_keyword)
        state = State(name=state, run_callback=run_callback, on_update_callback=on_update_callback)
        sm_instance.add_state(state)

    def go_to_state(self, state: str, sm: str) -> None:
        sm_instance = self._get_state_machine_or_raise_error(sm)
        sm_instance.go_to_state(state)

    def update_state(self, sm: str) -> None:
        sm_instance = self._get_state_machine_or_raise_error(sm)
        sm_instance.update()

    def get_context(self, sm: str) -> dict:
        sm_instance = self._get_state_machine_or_raise_error(sm)
        return sm_instance.context

    def set_context(self, sm: str, context: dict) -> None:
        sm_instance = self._get_state_machine_or_raise_error(sm)
        sm_instance.context = context

    def update_context(self, sm: str, item: dict) -> None:
        sm_instance = self._get_state_machine_or_raise_error(sm)
        sm_instance.context = dict_merge(sm_instance.context, item)

    def _get_state_machine_or_raise_error(self, sm: str) -> StateMachine:
        state_machine = self._store.get(sm)
        if state_machine is None:
            raise StateMachineNotFoundError(self.missing_state_machine_message.format(sm))
        return state_machine
