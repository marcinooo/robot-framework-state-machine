"""
Contains different utils for whole package.
"""

import copy
from typing import Callable
from robot.api import logger
from robot.running.model import Keyword
from robot.running.context import EXECUTION_CONTEXTS
from robot.libraries.BuiltIn import RobotNotRunningError
from robot.errors import DataError
from robot.running.usererrorhandler import UserErrorHandler


def get_keword(name: str) -> Keyword:
    """
    Returns Keyword object for given name.

    :param name: name of keyword
    :return: found keyword
    """

    return Keyword(name)


def get_robot_context(top: bool = False) -> EXECUTION_CONTEXTS:
    """
    Returns current robot context or raises RobotNotRunningError error.

    :param top: top context will be returned if it is True
    :return: robot context
    """

    ctx = EXECUTION_CONTEXTS.current if not top else EXECUTION_CONTEXTS.top
    if ctx is None:
        raise RobotNotRunningError('Cannot access execution context')
    return ctx


def keyword_should_exist(name: str) -> None:
    """
    Checks if keyword was defined.

    :param name: name of keyword
    :return: None
    """

    ctx = get_robot_context()
    try:
        runner = ctx.namespace.get_runner(name)
    except DataError as error:
        raise AssertionError(error.message)
    if isinstance(runner, UserErrorHandler):
        raise AssertionError(runner.error.message)


def is_string(item: object) -> bool:
    """
    Checks if passed argument is a string object.

    :param item: item for verify
    :return: Ture if item is string, otherwise False
    """

    return isinstance(item, str)


def is_dictionary(item: object) -> bool:
    """
    Checks if passed argument is a dictionary object.

    :param item: item for verify
    :return: Ture if item is dictionary, otherwise False
    """

    return isinstance(item, dict)


def build_callback(keyword: Keyword) -> Callable:
    """
    Returns function callback for `.state_machine.State` class.

    :param keyword: keyword which 'run' method will be executed in callback
    :return: callback function
    """

    def callback():
        context = get_robot_context()
        keyword.run(context)

    return callback


def dict_merge(a: dict, b: dict) -> dict:
    """
    Merges second dictionary to first. It does not modify any of dictionaries.

    :param a: first dictionary
    :param b: second dictionary
    :return: merged dictionary
    """

    if not is_dictionary(a):
        raise ValueError("Argument 'a' should be a dictionary")
    if not is_dictionary(b):
        return b

    result = copy.deepcopy(a)

    for k, v in b.items():
        if k in result and isinstance(result[k], dict):
            result[k] = dict_merge(result[k], v)
        else:
            result[k] = copy.deepcopy(v)

    return result


def log_state_machine_states(sm) -> None:
    """
    Logs all created state machines.

    :param sm: state machine instnace
    :return: None
    """

    logger.debug('States added to state machine:\n' + '\n'.join(f' - {state}' for state in sm.states.keys()))
