"""
Library facade.
"""

from typing import Union, Any, List, Dict
from itertools import count
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from .store import StateMachineStore
from .state_machine import StateMachine, State
from .exceptions import StateMachineNotFoundError, DefaultStateMachineNotFoundError
from .utils import (is_string, is_dictionary, get_keword, build_callback, dict_merge, keyword_should_exist,
                    log_state_machine_states)


class StateMachineFacade:
    """Facade provides api to create and manage state machines from robot code."""

    def __init__(self) -> None:
        self._store = StateMachineStore()

    def create_state_machine(self, sm_name: str) -> None:
        """Creates state machine object."""

        if not is_string(sm_name):
            raise RuntimeError('Name of state machine must be a string.')

        if self._store.get(sm_name) is not None:
            logger.warn('State machine named "{}" has been overwritten'.format(sm_name))

        sm = StateMachine(sm_name)
        self._store.add(sm_name, sm)

        logger.debug('State machine named "{}" was created.'.format(sm_name))

    def destroy_state_machine(self, sm_name: str) -> None:
        """Destroys state machine object."""

        if not is_string(sm_name):
            raise RuntimeError('Name of state machine must be a string.')

        if self._store.get(sm_name) is None:
            logger.warn('State machine named "{}" does not exist.'.format(sm_name))
        else:
            self._store.remove(sm_name)
            logger.debug('State machine with name "{}" was destroyed.'.format(sm_name))

    def run_state_machine(self,
                          sm_name: Union[str, None] = None,
                          start_from: Union[str, None] = None,
                          max_updates: Union[int, None] = -1) -> None:
        """Runs state machine. It calls continuously keyword to update state."""

        sm_instance = self._get_state_machine_from_store(sm_name)

        sm_instance.activate()

        if start_from is not None:
            BuiltIn().run_keyword('StateMachineLibrary.Go To State', start_from, sm_instance.name)

        for iteration in count(0):

            logger.debug(f'Iteration {iteration}:')
            BuiltIn().run_keyword('StateMachineLibrary.Update State', sm_instance.name)

            if iteration == max_updates - 1 or not sm_instance.is_active:
                break

        sm_instance.deactivate()

    def stop_state_machine(self, sm_name: Union[str, None] = None) -> None:
        """Stops state machine."""

        sm_instance = self._get_state_machine_from_store(sm_name)
        sm_instance.deactivate()

        logger.debug(f'State machine "{sm_instance.name}" was stopped.')

    def get_state_machine_states(self, sm_name: Union[str, None] = None) -> List[str]:
        """Gets list of states added to given state machine."""

        sm_instance = self._get_state_machine_from_store(sm_name)

        log_state_machine_states(sm_instance)

        return list(sm_instance.states.keys())

    def add_state(self, state: str, on_update: str, sm_name: Union[str, None] = None) -> None:
        """Adds single state to state machine."""

        if not is_string(state):
            raise RuntimeError('State parameter should be name of keyword with main state procedure.')
        if not is_string(on_update):
            raise RuntimeError('On update parameter should be name of keyword with transition procedure.')

        sm_instance = self._get_state_machine_from_store(sm_name)

        keyword_should_exist(state)
        keyword_should_exist(on_update)

        state_keyword = get_keword(state)
        on_update_keyword = get_keword(on_update)
        run_callback = build_callback(state_keyword)
        on_update_callback = build_callback(on_update_keyword)

        state_instance = State(name=state, run_callback=run_callback, on_update_callback=on_update_callback)
        sm_instance.add_state(state_instance)

        logger.debug('State with "{}" run keyword and "{}" update keyword was add to "{}" '
                     'state machine.'.format(state, on_update, sm_instance.name))

    def go_to_state(self, state: str, sm_name: Union[str, None] = None) -> None:
        """Jumps to specified state."""

        if not is_string(state):
            raise RuntimeError('State parameter should be name of keyword.')

        sm_instance = self._get_state_machine_from_store(sm_name)
        sm_instance.go_to_state(state)

    def update_state(self, sm_name: Union[str, None] = None) -> None:
        """Goes to next state."""

        sm_instance = self._get_state_machine_from_store(sm_name)
        sm_instance.update()

    def get_context(self, sm_name: Union[str, None] = None) -> Dict:
        """Returns context for given state machine."""

        sm_instance = self._get_state_machine_from_store(sm_name)
        return sm_instance.context

    def set_context(self, context: Dict, sm_name: Union[str, None] = None) -> None:
        """Overwrites context for given state machine."""

        if not is_dictionary(context):
            raise TypeError('Context parameter should be a dictionary.')

        sm_instance = self._get_state_machine_from_store(sm_name)
        sm_instance.context = context

    def update_context(self, sm_name: Union[str, None] = None, **items: Any) -> None:
        """Updates context for given state machine."""

        sm_instance = self._get_state_machine_from_store(sm_name)
        sm_instance.context = dict_merge(sm_instance.context, items)

    def _get_state_machine_from_store(self, sm_name: Union[str, None] = None) -> StateMachine:
        """
        Gets state machine by name from state machines store.
        If name is None and there is only one state machine in store it will return it as default.

        :param sm_name: name of state machine
        :return: state machine object
        :raises DefaultStateMachineNotFoundError: when there is no only one state machine in store
        :raises StateMachineNotFoundError: when there is no state machine with given name in store
        """

        if sm_name is None:

            all_state_machines = self._store.get_all()
            count_of_state_machines = len(all_state_machines)

            if count_of_state_machines > 1:
                logger.debug('All created state machines:\n' + ',\n'.join(all_state_machines))
                missing_default_message = ('There is more then one state machine in store. Indicate which '
                                           'state machine should be used e.g.: ... sm_name=name-of-sm ...')
                raise DefaultStateMachineNotFoundError(missing_default_message)

            if count_of_state_machines == 0:
                missing_default_message = ('There is no any state machines in store. '
                                           'Call keyword "Create State Machine" to create it.')
                raise DefaultStateMachineNotFoundError(missing_default_message)

            state_machine = list(all_state_machines.values())[0]

        else:

            state_machine = self._store.get(sm_name)

            if state_machine is None:
                logger.debug('All created state machines:\n' + ',\n'.join(self._store.get_all()))
                missing_state_machine_message = 'There is no state machine named "{}".\n' \
                                                'Call keyword "Create State Machine" to create it.'
                raise StateMachineNotFoundError(missing_state_machine_message.format(sm_name))

        return state_machine
