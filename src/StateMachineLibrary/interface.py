from .facade import StateMachineFacade


class StateMachineLibrary(object):

    def __init__(self) -> None:
        self._facade = StateMachineFacade()

    def create_state_machine(self, name) -> None:
        """
        Creates state machine object. State machine can control flow in your test or task definition.
        Example of flow:
            state A  ->  state B  ->  state C  ->  state A  ->  state B
                                              `->  state C
        :param name: name of state machine given by you
        :return: None
        """
        self._facade.create_state_machine(name)

    def add_state(self, run, on_update, sm) -> None:  # dodaj sprawdzanie czy state nie zawier go to...
        """
        Adds single state to state machine. To creates state you have to define state keyword
        which contains main code of state to execute. In addition you have to define a method that contains
        the transition logic to the next state.
        :param run: name of keyword with main state logic
        :param on_update: name of keyword with transition logic to the next state
        :param sm: name of state machine
        :return: None
        """
        self._facade.add_state(run, on_update, sm)

    def go_to_state(self, state, sm) -> None:
        """
        Jumps to specified state. State is identified by name of main keyword.

        .. warning::
            You can not use it in main keyword for given state.

        :param state: name of next keyword
        :param sm: name of state machine
        :return: None
        """
        self._facade.go_to_state(state, sm)

    def update_state(self, sm) -> None:
        """
        Goes to next state. It calls keyword with transition logic to the next state and main keyword from next state.
        Next state is indicated in keyword with transition logic for current state.
        :param sm: name of state machine
        :return: None
        """
        self._facade.update_state(sm)

    def get_context(self, sm: str) -> dict:
        """
        Returns context for given state machine. Context is dictionary where you can store common resources
        for state machine.
        :param sm: name of state machine
        :return: context as dictionary
        """
        return self._facade.get_context(sm)

    def set_context(self, sm: str, context: dict) -> None:
        """
        Overwrites context for given state machine. All common resources for state machine will be overwritten.
        :param sm: name of state machine
        :param context: context to set
        :return: None
        """
        self._facade.set_context(sm, context)

    def update_context(self, sm: str, item: dict) -> None:  # dodac zwracanie kontekstu
        """
        Updates context for given state machine. It merges passed dictionary item with existing context.
        Example:
            +---------------------+------------------------------------+------------------------------------+
            | existing context    | item                               | result                             |
            +=====================+====================================+====================================+
            | {'result':{}}       | {'result':{'status':'FINISHED'}}   | {'result':{'status':'FINISHED'}}   |
            +---------------------+------------------------------------+------------------------------------+
            | {'time':'00:00'}    | {'user':'Leo'}                     | {'time':'00:00','user':'Leo'}      |
            +---------------------+------------------------------------+------------------------------------+
            | {'errors':0}        | {'errors':1}                       | {'errors':1}                       |
            +---------------------+------------------------------------+------------------------------------+

        :param sm: name of state machine
        :param item: object to add to context
        :return: None
        """
        self._facade.update_context(sm, item)

    def destroy_state_machine(self, name) -> None:
        """
        Destroys state machine object.
        :param name: name of created state machine
        :return: None
        """
        self._facade.destroy_state_machine(name)
