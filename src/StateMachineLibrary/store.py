"""
Contains implementation of store to collect all state machines.
"""

from typing import Union, Dict

from .state_machine import StateMachine


class StateMachineStore:
    """Local store for all state machines."""

    _STORE = {}
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StateMachineStore, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def add(self, name: str, sm: StateMachine) -> None:
        """
        Adds state machine with given name to store.

        :param name: name for state machine
        :param sm: state machine object
        :return: None
        """

        self._STORE[name] = sm

    def get(self, name: str) -> Union[StateMachine, None]:
        """
        Returns state machine from store.

        :param name: name of state machine
        :return: state machine if it was found otherwise None
        """

        return self._STORE.get(name)

    def remove(self, name: str) -> Union[StateMachine, None]:
        """
        Removes state machine with given name from store.

        :param name: name of state machine
        :return: removed state machine
        """

        return self._STORE.pop(name, None)

    def get_all(self) -> Dict[str, StateMachine]:
        """
        Returns all stored state machines.

        :return: dictionary of names and state machines
        """

        return self._STORE
