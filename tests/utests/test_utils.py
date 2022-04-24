import os
import sys
import pytest

test_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(test_dir, '..', '..', 'src'))

from StateMachineLibrary.utils import dict_merge


@pytest.mark.parametrize("dict_a,dict_b,result", (
    (
        {},
        {'status': 'UNKNOWN'},
        {'status': 'UNKNOWN'},
    ),
    (
        {'status': 'UNKNOWN'},
        {},
        {'status': 'UNKNOWN'},
    ),
    (
        {'name': 'Martin'},
        {'age': 12},
        {'name': 'Martin', 'age': 12},
    ),
    (
        {'develoers': {'Martin': {'age': 25}, 'Joe': {}}},
        {'develoers': {'Mark': {'age': 22}, 'Joe': {'age': 29}}},
        {'develoers': {'Martin': {'age': 25}, 'Mark': {'age': 22}, 'Joe': {'age': 29}}},
    ),
    (
        {'users': [{'name': 'Martin', 'age': 12}]},
        {'users': [{'name': 'Martin', 'age': 13}]},
        {'users': [{'name': 'Martin', 'age': 13}]},
    ),
    (
        {'statistics': None},
        1,
        1,
    ),
))
def test_dict_merge_with_valid_parameters(dict_a, dict_b, result):
    assert dict_merge(dict_a, dict_b) == result


@pytest.mark.parametrize("dict_a,dict_b,expected_error", (
    (
        1,
        {'statistics': None},
        "Argument 'a' should be a dictionary",
    ),
))
def test_dict_merge_with_invalid_parameters(dict_a, dict_b, expected_error):
    with pytest.raises(Exception) as excinfo:
        _ = dict_merge(dict_a, dict_b)
    assert str(excinfo.value) == expected_error
