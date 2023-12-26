"""
Collections of exceptions raises by package.
"""


class StateMachineBaseError(Exception):
    """Base library exception."""


class StateMachineNotFoundError(StateMachineBaseError):
    """Throws when state machine was not found."""


class StateNotFoundError(StateMachineBaseError):
    """Throws when state was not added to state machine."""


class CurrentStateNotDefinedError(StateMachineBaseError):
    """Throws when state machine updates state but current state was not set."""


class DefaultStateMachineNotFoundError(StateMachineBaseError):
    """Throws when default state machine was not found."""
