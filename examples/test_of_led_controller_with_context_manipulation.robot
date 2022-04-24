*** Settings ***
Library  Collections
Library  StateMachineLibrary


*** Test Cases ***
Control Led
    [setup]  Run Keywords
    ...  Create State Machine            name=led-machine                                   AND
    ...  Add State  state=Waiting State  on_update=On Update Waiting State  sm=led-machine  AND
    ...  Add State  state=Led On State   on_update=On Update Led On State   sm=led-machine  AND
    ...  Add State  state=Led Off State  on_update=On Update Led Off State  sm=led-machine

    Go To State  state=Led Off State  sm=led-machine
    Repeat Keyword	10 times  Update State  sm=led-machine


*** Keywords ***
Waiting State
    [Documentation]  Wait for switch update.
    Log To Console  Waiting...
    WHILE  ${True}  limit=NONE
        ${is_swiched}=  Get Swich Status
        IF  ${is_swiched}
            BREAK
        END
    END

On Update Waiting State
    &{context}=  Get Context  sm=led-machine
    IF  '${context["led_state"]}'=='on'
        Go To State  state=Led Off State  sm=led-machine
    ELSE
        Go To State  state=Led On State  sm=led-machine
    END

Led On State
    [Documentation]  Turn light on.
    Log To Console  LED is ON
    &{item}=  Create Dictionary  led_state=on
    Update Context  sm=led-machine  item=${item}

On Update Led On State
    Go To State  state=Waiting State  sm=led-machine

Led Off State
    [Documentation]  Turn light off. 
    Log To Console  LED is OFF
    &{item}=  Create Dictionary  led_state=off
    Update Context  sm=led-machine  item=${item}

On Update Led Off State
    &{context}=  Get Context  sm=led-machine
    Go To State  state=Waiting State  sm=led-machine

Get Swich Status
    [Documentation]  It is mock keyword testing if switch was switched. 
    [return]  ${True}
