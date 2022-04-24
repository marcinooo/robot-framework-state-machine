import copy
from typing import Callable
from robot.api import logger
from robot.running.model import Keyword
from robot.running.context import EXECUTION_CONTEXTS
from robot.libraries.BuiltIn import RobotNotRunningError
from robot.errors import DataError
from robot.running.usererrorhandler import UserErrorHandler


def get_keword(name: str) -> Keyword:
    return Keyword(name)


def get_robot_context(top: bool = False):
    ctx = EXECUTION_CONTEXTS.current if not top else EXECUTION_CONTEXTS.top
    if ctx is None:
        raise RobotNotRunningError('Cannot access execution context')
    return ctx


def keyword_should_exist(name: str) -> None:
    ctx = get_robot_context()
    try:
        runner = ctx.namespace.get_runner(name)
    except DataError as error:
        raise AssertionError(error.message)
    if isinstance(runner, UserErrorHandler):
        raise AssertionError(runner.error.message)


def is_string(item: object) -> bool:
    return isinstance(item, str)


def is_dictionary(item: dict) -> bool:
    return isinstance(item, dict)


def build_callback(keyword: Keyword) -> Callable:
    def callback():
        context = get_robot_context()
        keyword.run(context)
    return callback


def dict_merge(a: dict, b: dict) -> dict:
    if not isinstance(a, dict):
        raise ValueError("Argument 'a' should be a dictionary")
    if not isinstance(b, dict):
        return b 
    result = copy.deepcopy(a)
    for k, v in b.items():
        if k in result and isinstance(result[k], dict):
            result[k] = dict_merge(result[k], v)
        else:
            result[k] = copy.deepcopy(v)
    return result


def log_state_machine_states(sm) -> None:
    logger.debug('States added to state machine:\n' + ',\n'.join(sm.states.keys()))
