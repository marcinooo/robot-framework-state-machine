import os
import sys
import pytest

test_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(test_dir, '..', '..', 'src'))

from StateMachineLibrary.store import StateMachineStore
from StateMachineLibrary.state_machine import StateMachine


@pytest.fixture
def state_machine_a():
    state_machine = StateMachine('test-state-machine-A')
    return state_machine


@pytest.fixture
def state_machine_b():
    state_machine = StateMachine('test-state-machine-B')
    return state_machine


def test_add_state(state_machine_a, state_machine_b):
    store = StateMachineStore()
    store.add(state_machine_a.name, state_machine_a)
    store = StateMachineStore()
    store.add(state_machine_b.name, state_machine_b)
    store = StateMachineStore()
    assert store.get(state_machine_a.name) is not None and store.get(state_machine_b.name) is not None
