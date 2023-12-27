=================================
State Machine for Robot Framework
=================================

.. image:: https://dl.circleci.com/status-badge/img/gh/marcinooo/robot-framework-state-machine/tree/main.svg?style=svg
    :target: https://dl.circleci.com/status-badge/redirect/gh/marcinooo/robot-framework-state-machine/tree/main

|

:Author: marcinooo
:Tags: Robot Framework, Python, State Machine, Library

:abstract:

   Implementation of state machine in robot framework.

.. contents ::

Description
===========

Library contains implementation of state machine
to control or test software components which can be in many states.

Documentation
-------------

Library documentation can be found `here <https://robot-framework-state-machine.readthedocs.io/en/latest/>`_.

A good starting point is to check examples:

- `basic example <https://github.com/marcinooo/robot-framework-state-machine/blob/master/examples/test_rest_api_of_led_controller>`_
- `usage of library in python code <https://github.com/marcinooo/robot-framework-state-machine/blob/master/examples/task_to_generate_data_transmission_report>`_
- `usage of two state machines <https://github.com/marcinooo/robot-framework-state-machine/blob/master/examples/test_two_products_with_two_state_machines>`_


Installation
============

Install from PyPI:

``$ pip install robotframework-statemachinelibrary``

Install from github:

``$ pip install git+https://github.com/marcinooo/robot-framework-state-machine``


Usage
=====

An example of using the library for LED blinking (of course, the library was created for more complex tasks :wink:).

.. code:: robotframework

    *** Settings ***
    Library  StateMachineLibrary

    *** Tasks ***
    Blink
        [setup]  Task Setup
        Run State Machine  start_from=Turn On Light  max_updates=10

    *** Keywords ***
    Task Setup
        Create State Machine  name=blink-machine
        Add State  state=Turn On Light   on_update=On Update Turn On Light
        Add State  state=Turn Off Light  on_update=On Update Turn Off Light

    Turn On Light
        Log To Console  I am ON

    On Update Turn On Light
        Sleep  0.25s
        Go To State  state=Turn Off Light

    Turn Off Light
        Log To Console  I am OFF

    On Update Turn Off Light
        Sleep  0.25s
        Go To State  state=Turn On Light


Flow diagram:

.. image:: https://raw.githubusercontent.com/marcinooo/robot-framework-state-machine/main/states_flow.png
    :width: 760
    :alt: Flow diagram for above code


Overview
--------

First of all import the library:

.. code:: robotframework

    Library  StateMachineLibrary

Create a state machine:

.. code:: robotframework

    Create State Machine  name=blink-machine

You can create as many as you want state machines. Each state machine should have a unique name.

Register keywords that should be executed in the given state (*Turn On Light*) and during its update (*On Update Turn On Light*):

.. code:: robotframework

    Add State  state=Turn On Light   on_update=On Update Turn On Light

Both keywords must be defined:

.. code:: robotframework

    *** Keywords ***
    # ...
    Turn On Light
        # Here you can put logic (e.g.: led controller)
        Log To Console  I am ON

    On Update Turn On Light
        Go To State  state=Turn Off Light

Keywords *On Update...* should indicate the next state:

.. code:: robotframework

    Go To State  state=Turn Off Light

Call the same keyword to enter the first state.

Force transition to a next state:

.. code:: robotframework

    Update State

You can pass data between states in **context** (recommended method) or using global variables.

.. code:: robotframework

    *** Keywords ***
    # ...

    Turn On Light
        Update Context  led_status=ON

    Turn Off Light
        # ...
        &{context}=    Get Context
        Log To Console    LED is ${context["led_status"]}


License
=======

license_ (MIT)

.. _license: https://github.com/marcinooo/robot-framework-state-machine/blob/main/LICENSE.txt
