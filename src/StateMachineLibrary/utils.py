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


# def merge_dictionaries(dict_a, dict_b):
#     """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
#     updating only top-level keys, dict_merge recurses down into dicts nested
#     to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
#     ``dct``.
#     :param dct: dict onto which the merge is executed
#     :param merge_dct: dct merged into dct
#     :return: None
#     """
#     for k, v in dict_b.iteritems():
#         if k in dict_a and isinstance(dict_a[k], dict) and isinstance(dict_b[k], collections.Mapping):
#             merge_dictionaries(dict_a[k], dict_b[k])
#         else:
#             dict_a[k] = dict_b[k]

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
