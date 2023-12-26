import pytest

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
    assert store.get(state_machine_a.name) is not None
    assert store.get(state_machine_b.name) is not None
