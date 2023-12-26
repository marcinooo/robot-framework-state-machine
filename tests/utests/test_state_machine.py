import os
import sys
import pytest

test_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(test_dir, '..', '..', 'src'))

from StateMachineLibrary.state_machine import StateMachine, State


@pytest.fixture
def state_machine():
    state_machine = StateMachine('test-state-machine')
    return state_machine


@pytest.mark.parametrize("names", (
    ('simple-state',),
    ('first-state', 'second-state', 'third-state'),
))
def test_add_state(names, state_machine):
    for name in names:
        state = State(name, lambda: None, lambda: None)
        state_machine.add_state(state)
    added_names = [name for name in names if name in state_machine.states.keys()]
    assert added_names and all(added_names)


@pytest.mark.parametrize("names", (
    ('simple-state',),
    ('first-state', 'second-state', 'third-state'),
))
def test_go_to_state(names, state_machine):
    results_of_state_run = []
    for name in names:
        state = State(name, lambda: results_of_state_run.append(name), lambda: None)
        state_machine.states.update({state.name: state})
        state_machine.go_to_state(name)
    assert list(names) == results_of_state_run


@pytest.mark.parametrize("names", (
    ('simple-state',),
    ('first-state', 'second-state', 'third-state'),
))
def test_update(names, state_machine):
    results_of_state_on_update = []
    for name in names:
        state = State(name, lambda: None, lambda: results_of_state_on_update.append(name))
        state_machine.states.update({state.name: state})
        state_machine.current_state = state_machine.states[name]
        state_machine.update()
    assert list(names) == results_of_state_on_update
