from .facade import StateMachineFacade


class StateMachineLibrary(object):

    def __init__(self) -> None:
        self._facade = StateMachineFacade()

    def create_state_machine(self, name: str) -> None:
        self._facade.create_state_machine(name)

    def add_state(self, state: str, on_update: str, sm: str) -> None:
        self._facade.add_state(state, on_update, sm)

    def go_to_state(self, state: str, sm: str) -> None:
        self._facade.go_to_state(state, sm)

    def update_state(self, sm: str) -> None:
        self._facade.update_state(sm)

    def get_context(self, sm: str):
        return self._facade.get_context(sm)

    def set_context(self, sm: str, context):
        self._facade.set_context(sm, context)

    def update_context(self, sm: str, item: dict):
        self._facade.update_context(sm, item)
