*** Settings ***
Library  StateMachineLibrary


*** Tasks ***
Calculate the sum of 2 numbers
    [setup]  Task Setup
    Go To State  state=Get First Number  sm=calc-machine
    Repeat Keyword	4 times  Update State  sm=calc-machine


*** Keywords ***
Task Setup
    Create State Machine  name=calc-machine
    Add State  state=Get First Number   on_update=On Update Get First Number  sm=calc-machine
    Add State  state=Get Second Number  on_update=On Update Get Second Number   sm=calc-machine
    Add State  state=Add Numbers        on_update=On Update Add Numbers  sm=calc-machine
    Add State  state=Return result      on_update=On Update Return result  sm=calc-machine
    Log To Console  ${EMPTY}

Get First Number
    Log To Console  Get the first number...

On Update Get First Number
    Go To State  state=Get Second Number  sm=calc-machine

Get Second Number
    Log To Console  Get the second number...

On Update Get Second Number
    Go To State  state=Add Numbers  sm=calc-machine

Add Numbers
    Log To Console  Add two numbers...

On Update Add Numbers
    Go To State  state=Return result  sm=calc-machine

Return result
    Log To Console  Return result...

On Update Return result
    No Operation
