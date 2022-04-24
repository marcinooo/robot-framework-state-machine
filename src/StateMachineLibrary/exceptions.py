"""
Collections of exceptions raises by package.
"""


class StateMachineNotFoundError(Exception):
    """Error indicates that state machine was not found."""


class StateNotFoundError(Exception):
    """Error indicates that state was not added to state machine."""
