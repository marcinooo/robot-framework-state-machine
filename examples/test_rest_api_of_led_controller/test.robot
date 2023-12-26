*** Settings ***

Library  StateMachineLibrary
Library  OperatingSystem
Library  RequestsLibrary


*** Variables ***

${BASE_URL}  http://127.0.0.1:8000
&{HEADERS}   Content-Type=application/json


*** Test Cases ***

Test LED Controller REST API
    [setup]  Test Setup
    Run State Machine  max_updates=10  start_from=Set LED Controller State


*** Keywords ***

Test Setup
    # Set no_proxy environment variable to request localhost server (python's requests module requires it)
    Set Environment Variable  no_proxy  127.0.0.1,localhost

    Create State Machine  sm_name=led-controller-machine

    Add State  state=Check LED Controller State
    ...        on_update=On Update Check LED Controller State
    Add State  state=Set LED Controller State
    ...        on_update=On Update Set LED Controller State
    Add State  state=Clear LED Controller State
    ...        on_update=On Update Clear LED Controller State

Check LED Controller State
    [Documentation]  Checkes if LED has expected status (which is read from state machine context).

    ${response}=  GET  ${BASE_URL}/led-controller  headers=${HEADERS}
    &{context}=  Get Context
    Should Be Equal As Strings  ${context}[expected_status]  ${response.json()}[status]

On Update Check LED Controller State
    [Documentation]  Navigates to set oposite state of LED.

    &{context}=  Get Context
    IF  '${context}[expected_status]'=='off'
        Go To State  state=Set LED Controller State
    ELSE
        Go To State  state=Clear LED Controller State
    END

Set LED Controller State
    [Documentation]  Turns on LED.

    ${response}=  GET  ${BASE_URL}/led-controller  params=status=on  headers=${HEADERS}
    # Verifies response returned from server
    Should Be Equal As Strings  on  ${response.json()}[status]
    # Verifies expected value of LED to check
    Update Context  expected_status=on

On Update Set LED Controller State
    Go To State  state=Check LED Controller State

Clear LED Controller State
    [Documentation]  Turns on LED.

    ${response}=  GET  ${BASE_URL}/led-controller  params=status=off  headers=${HEADERS}
    # Verifies response returned from sever
    Should Be Equal As Strings  off  ${response.json()}[status]
    # Verifies expected value of LED to check
    Update Context  expected_status=off

On Update Clear LED Controller State
    Go To State  state=Check LED Controller State
