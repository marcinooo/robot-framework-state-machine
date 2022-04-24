*** Settings ***
Library  Collections
Library  StateMachineLibrary


*** Variables ***
@{fake_list}=    Create List    a    b    c
${error_invalid_state_machine_name}=    Name of state machine must be a string.
${error_invalid_run_keyword_name}=    State parameter should be name of keyword with main state procedure.
${error_invalid_on_update_keyword_name}=    On update parameter should be name of keyword with transition procedure.
${error_invalid_go_to_state_keyword_name}=    State parameter should be name of keyword.
${error_invalid_name_of_created_state_machine}=    Sm parameter should be name of created state machine.


*** Test Cases ***
Test Create And Destroy State Machine
    Create State Machine    name=simple-machine

    Create State Machine    name=Other Machine

    Run Keyword And Expect Error    ${error_invalid_state_machine_name}
    ...    Create State Machine    name=${0}

    Run Keyword And Expect Error    ${error_invalid_state_machine_name}
    ...    Create State Machine    name=${fake_list}

    Destroy State Machine    name=simple-machine

    Destroy State Machine    name=Other Machine

    Run Keyword And Expect Error    ${error_invalid_state_machine_name}
    ...    Destroy State Machine    name=${0}

    Run Keyword And Expect Error    ${error_invalid_state_machine_name}
    ...    Destroy State Machine    name=${fake_list}


Add State to State Machine
    [Setup]    Create State Machine    name=test-machine
    Add State    state=Fake State    on_update=On Update Fake State    sm=test-machine

    Run Keyword And Expect Error    ${error_invalid_state_machine_name}
    ...    Add State    state=Fake State    on_update=On Update Fake State    sm=${0}

    Run Keyword And Expect Error    ${error_invalid_run_keyword_name}
    ...    Add State    state=${0}    on_update=On Update Fake State    sm=test-machine

    Run Keyword And Expect Error    ${error_invalid_on_update_keyword_name}
    ...    Add State    state=Fake State    on_update=${0}    sm=test-machine

    Run Keyword And Expect Error    ${error_invalid_run_keyword_name}
    ...    Add State    state=${fake_list}    on_update=On Update Fake State    sm=test-machine

    Run Keyword And Expect Error    ${error_invalid_on_update_keyword_name}
    ...    Add State    state=Fake State    on_update=${fake_list}    sm=test-machine

    [Teardown]    Destroy State Machine    name=test-machine


Test Go To State
    [Setup]    Run Keywords
    ...        Create State Machine    name=test-machine    AND
    ...        Add State    state=Fake State To Set Variable    on_update=On Update Fake State    sm=test-machine    AND
    ...        Set Test Variable    ${go_to_keyword_success}    ${False}

    Go To State    state=Fake State To Set Variable    sm=test-machine
    Should Be True    ${go_to_keyword_success}

    Run Keyword And Expect Error    ${error_invalid_name_of_created_state_machine}
    ...    Go To State    state=Fake State    sm=${0}

    Run Keyword And Expect Error    ${error_invalid_go_to_state_keyword_name}
    ...    Go To State    state=${0}    sm=test-machine

    [Teardown]    Destroy State Machine    name=test-machine


Test Update State
    [Setup]    Run Keywords
    ...        Create State Machine    name=test-machine    AND
    ...        Add State    state=Fake State    on_update=On Update Fake State To Set Variable    sm=test-machine    AND
    ...        Add State    state=Fake State To Set Variable    on_update=On Update Fake State    sm=test-machine    AND
    ...        Go To State    state=Fake State    sm=test-machine    AND
    ...        Set Test Variable    ${on_update_keyword_success}    ${False}    AND
    ...        Set Test Variable    ${go_to_keyword_success}    ${False}

    Update State    sm=test-machine
    Should Be True    ${go_to_keyword_success}
    Should Be True    ${on_update_keyword_success}

    Run Keyword And Expect Error    ${error_invalid_name_of_created_state_machine}
    ...    Update State    sm=${0}

    [Teardown]    Destroy State Machine    name=test-machine


*** Keywords ***
Fake State
    No Operation

On Update Fake State
    No Operation

Fake State To Set Variable
    Set Test Variable    ${go_to_keyword_success}    ${True}

On Update Fake State To Set Variable
    Set Test Variable    ${on_update_keyword_success}    ${True}
    Go To State    state=Fake State To Set Variable    sm=test-machine
