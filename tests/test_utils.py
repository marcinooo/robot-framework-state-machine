import os
import sys
import pytest

test_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(test_dir, '..', 'src'))

from StateMachineLibrary.utils import dict_merge


@pytest.mark.parametrize("dict_a,dict_b,result,expect_error", (
    (
        {}, 
        {'status': 'UNKNOWN'},
        {'status': 'UNKNOWN'},
        False
    ),
    (
        {'status': 'UNKNOWN'},
        {}, 
        {'status': 'UNKNOWN'},
        False
    ),
    (
        {'name': 'Martin'}, 
        {'age': 12}, 
        {'name': 'Martin', 'age': 12},
        False
    ),
    (
        {'develoers': {'Martin': {'age': 25}, 'Joe': {}}}, 
        {'develoers': {'Mark': {'age': 22}, 'Joe': {'age': 29}}}, 
        {'develoers': {'Martin': {'age': 25}, 'Mark': {'age': 22}, 'Joe': {'age': 29}}},
        False
    ),
    (
        {'users': [{'name': 'Martin', 'age': 12}]}, 
        {'users': [{'name': 'Martin', 'age': 13}]},
        {'users': [{'name': 'Martin', 'age': 13}]},
        False
    ),
    (
        {'statistics': None}, 
        1, 
        1,
        False
    ),
    (
        1,
        {'statistics': None}, 
        "Argument 'a' should be a dictionary",
        True
    ),
))
def test_dict_merge(dict_a, dict_b, result, expect_error):
    if expect_error:
        with pytest.raises(Exception) as excinfo:
            _ = dict_merge(dict_a, dict_b)
        assert str(excinfo.value) == result
    else:
        assert dict_merge(dict_a, dict_b) == result
