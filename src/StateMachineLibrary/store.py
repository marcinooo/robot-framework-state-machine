from .state_machine import StateMachine


class StateMachineStore(object):

    _STORE = {}

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StateMachineStore, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def add(self, name: str, sm: StateMachine) -> None:
        self._STORE[name] = sm
    
    def get(self, name: str) -> StateMachine:
        return self._STORE.get(name)

    def remove(self, name: str) -> None:
        try:
            del  self._STORE[name]
        except KeyError:
            pass
