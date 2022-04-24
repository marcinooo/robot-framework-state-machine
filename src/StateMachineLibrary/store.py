from .state_machine import StateMachine


class StateMachineStore(object):
    """Stores all state machines."""
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
    
    def get(self, name: str) -> StateMachine:
        """
        Returns state machine which is in store.
        :param name: name of state machine
        :return: state machine if it was found otherwise None
        """
        return self._STORE.get(name)

    def remove(self, name: str) -> None:
        """
        Removes state machine from store.
        :param name: name of state machine
        :return: None
        """
        try:
            del self._STORE[name]
        except KeyError:
            pass

    def get_all(self):
        """
        Returns all stored state machines.
        :return: dictionary with names and state machines
        """
        return self._STORE
