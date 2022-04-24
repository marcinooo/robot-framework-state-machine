=================================
State Machine for Robot Framework
=================================

.. image:: https://circleci.com/gh/marcinooo/robot-framework-state-machine.svg?style=svg
    :target: https://circleci.com/gh/marcinooo/robot-framework-state-machine

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

Usage
=====

.. code:: robotframework

    *** Settings ***
    Library  StateMachineLibrary

    *** Test Case ***
    Blink
        [setup]  Task Setup
        Go To State  state=Turn On Light  sm=blink-machine
        Repeat Keyword	100 times  Update State  sm=blink-machine

    *** Keywords ***
    Task Setup
        Create State Machine  name=blink-machine
        Add State  state=Turn On Light   on_update=On Update Turn On Light   sm=blink-machine
        Add State  state=Turn Off Light  on_update=On Update Turn Off Light  sm=blink-machine

    Turn On Light
        Log To Console  Turn On Light...

    On Update Turn On Light
        Go To State  state=Turn Off Light  sm=blink-machine

    Turn Off Light
        Log To Console  Turn Off Light...

    On Update Turn Off Light
        Go To State  state=Turn On Light   sm=blink-machine


Installation
============

`$ pip install git+https://github.com/marcinooo/robot-framework-state-machine/tree/main`

License
=======

license_ (MIT)

.. _license: https://github.com/martinwac/air_purifier/blob/master/LICENSE.txt
