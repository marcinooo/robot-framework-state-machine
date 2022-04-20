import copy

from robot.running.model import Keyword
from robot.running.context import EXECUTION_CONTEXTS
from robot.libraries.BuiltIn import RobotNotRunningError


def get_keword(name):
    return Keyword(name)


def get_context(top=False):
    ctx = EXECUTION_CONTEXTS.current if not top else EXECUTION_CONTEXTS.top
    if ctx is None:
        raise RobotNotRunningError('Cannot access execution context')
    return ctx


def is_string(item):
    return isinstance(item, str)


def build_callback(keyword):
    def callback():
        context = get_context()
        keyword.run(context)
    return callback


def dict_merge(a, b):
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
