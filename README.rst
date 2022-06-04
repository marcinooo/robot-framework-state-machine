=================================
State Machine for Robot Framework
=================================

.. image:: https://circleci.com/gh/marcinooo/robot-framework-state-machine/tree/main.svg?style=svg
    :target: https://circleci.com/gh/marcinooo/robot-framework-state-machine/?branch=main

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

An example of using the library for LED blinking (of course, the library was created for more complex tasks :wink:).

.. code:: robotframework

    *** Settings ***
    Library  StateMachineLibrary

    *** Tasks ***
    Blink
        [setup]  Task Setup
        Go To State  state=Turn On Light  sm=blink-machine
        Repeat Keyword  100 times  Update State  sm=blink-machine

    *** Keywords ***
    Task Setup
        Create State Machine  name=blink-machine
        Add State  state=Turn On Light   on_update=On Update Turn On Light   sm=blink-machine
        Add State  state=Turn Off Light  on_update=On Update Turn Off Light  sm=blink-machine

    Turn On Light
        Log To Console  Turn On Light...
    #    Sleep    0.5s    # if you have real led then you need this ;)

    On Update Turn On Light
        Go To State  state=Turn Off Light  sm=blink-machine

    Turn Off Light
        Log To Console  Turn Off Light...
    #    Sleep    0.5s    # if you have real led then you need this ;)

    On Update Turn Off Light
        Go To State  state=Turn On Light   sm=blink-machine


Flow diagram:

.. image:: states_flow.png
    :width: 760
    :alt: Flow diagram for above code


Installation
============

Install from github:

`$ pip install git+https://github.com/marcinooo/robot-framework-state-machine`

License
=======

license_ (MIT)

.. _license: https://github.com/marcinooo/robot-framework-state-machine/blob/main/LICENSE.txt
