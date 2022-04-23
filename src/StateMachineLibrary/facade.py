from robot.api import logger

from .store import StateMachineStore
from .state_machine import StateMachine, State
from .utils import is_string, is_dictionary, get_keword, build_callback, dict_merge, keyword_should_exist
from .exceptions import StateMachineNotFoundError


class StateMachineFacade(object):
    """Provides api to create and manage state machine."""
    missing_state_machine_message = "There is no state machine named '{}'.\n" \
                                    "Call keyword 'Create State Machine' to create it."

    def __init__(self) -> None:
        self._store = StateMachineStore()

    def create_state_machine(self, name: str) -> None:
        """Creates state machine object."""
        if not is_string(name):
            raise RuntimeError('Name of state machine must be a string.')
        if self._store.get(name) is not None:
            logger.warn('State machine named {} has been overwritten'.format(name))
        sm = StateMachine(name)
        self._store.add(name, sm)
        logger.debug("State machine with name '{}' was created.".format(name))

    def add_state(self, run: str, on_update: str, sm: str) -> None:
        """Adds single state to state machine."""
        if not is_string(run):
            raise RuntimeError('Run parameter should be name of keyword with main state procedure.')
        if not is_string(on_update):
            raise RuntimeError('On update parameter should be name of keyword with main state procedure.')
        if not is_string(sm):
            raise RuntimeError('Sm parameter should be name of created state machine.')
        sm_instance = self._get_state_machine_or_raise_error(sm)
        keyword_should_exist(run)
        keyword_should_exist(on_update)
        state_keyword = get_keword(run)
        on_update_keyword = get_keword(on_update)
        run_callback = build_callback(state_keyword)
        on_update_callback = build_callback(on_update_keyword)
        state = State(name=run, run_callback=run_callback, on_update_callback=on_update_callback)
        sm_instance.add_state(state)
        logger.debug("State with '{}' run keyword "
                     "and '{}' update keyword was add to '{}' state machine.".format(run, on_update, sm))

    def go_to_state(self, state: str, sm: str) -> None:
        """Jumps to specified state."""
        if not is_string(state):
            raise RuntimeError('State parameter should be name of keyword.')
        if not is_string(sm):
            raise RuntimeError('Sm parameter should be name of created state machine.')
        sm_instance = self._get_state_machine_or_raise_error(sm)
        sm_instance.go_to_state(state)

    def update_state(self, sm: str) -> None:
        """Goes to next state."""
        if not is_string(sm):
            raise RuntimeError('Sm parameter should be name of created state machine.')
        sm_instance = self._get_state_machine_or_raise_error(sm)
        sm_instance.update()

    def get_context(self, sm: str) -> dict:
        """Returns context for given state machine."""
        if not is_string(sm):
            raise RuntimeError('Sm parameter should be name of created state machine.')
        sm_instance = self._get_state_machine_or_raise_error(sm)
        return sm_instance.context

    def set_context(self, sm: str, context: dict) -> None:
        """Overwrites context for given state machine."""
        if not is_string(sm):
            raise RuntimeError('Sm parameter should be name of created state machine.')
        if not is_dictionary(context):
            raise RuntimeError('Context parameter should be a dictionary.')
        sm_instance = self._get_state_machine_or_raise_error(sm)
        sm_instance.context = context

    def update_context(self, sm: str, item: dict) -> None:
        """Updates context for given state machine."""
        if not is_string(sm):
            raise RuntimeError('Sm parameter should be name of created state machine.')
        if not is_dictionary(item):
            raise RuntimeError('Item parameter should be a dictionary.')
        sm_instance = self._get_state_machine_or_raise_error(sm)
        sm_instance.context = dict_merge(sm_instance.context, item)

    def _get_state_machine_or_raise_error(self, sm: str) -> StateMachine:
        """
        Gets state machine with passed name or raises error if state machine does not exist.
        :param sm: name of state machine
        :return: state machine object
        """
        state_machine = self._store.get(sm)
        if state_machine is None:
            logger.debug('All created state machines:\n' + ',\n'.join(self._store.get_all()))
            raise StateMachineNotFoundError(self.missing_state_machine_message.format(sm))
        return state_machine
