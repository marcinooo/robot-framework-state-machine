*** Settings ***
Library  Collections
Library  StateMachineLibrary


*** Variables ***
${first_sm_name}   first_sm_name
${second_sm_name}  second_sm_name


*** Test Cases ***

Test Usage Of Single State Machine
    Create State Machine  sm_name=${first_sm_name}

    Add State  state=Fake Source State  on_update=On Update Fake Source State
    Add State  state=Fake Destination State  on_update=On Update Fake Destination State
    Run Keyword And Expect Error  No keyword with name 'Keyword Not Exists' found.
    ...                           Add State  state=Keyword Not Exists
    ...                                      on_update=On Update Fake Source State
    Run Keyword And Expect Error  No keyword with name 'On Update Keyword Not Exists' found.
    ...                           Add State  state=Fake Source State
    ...                                      on_update=On Update Keyword Not Exists

    Go To State  Fake Source State
    &{context}  Get Context
    Should Be Equal  ${context['executed']}  source
    Run Keyword And Expect Error  StateNotFoundError: State "Keyword Not Exists" was not added to "${first_sm_name}" state machine.
    ...                           Go To State  Keyword Not Exists
    Update Context  executed=null
    &{context}  Get Context
    Should Be Equal  ${context['executed']}  null
    Go To State  Fake Source State
    &{context}  Get Context
    Should Be Equal  ${context['executed']}  source

    Run State Machine

    &{context}  Get Context
    Should Be Equal  ${context['executed']}  destination

    Destroy State Machine  sm_name=${first_sm_name}


Test Usage Of Many State Machine
    Create State Machine  sm_name=${first_sm_name}
    Create State Machine  sm_name=${second_sm_name}

    Add State  state=Fake Source State
    ...        on_update=On Update Fake Source State
    ...        sm_name=${first_sm_name}
    Add State  state=Fake Destination State
    ...        on_update=On Update Fake Destination State
    ...        sm_name=${first_sm_name}
    Add State  state=Second Fake Source State
    ...        on_update=On Update Second Fake Source State
    ...        sm_name=${second_sm_name}
    Add State  state=Second Fake Destination State
    ...        on_update=On Update Second Fake Destination State
    ...        sm_name=${second_sm_name}
    ${msg}=  Catenate  DefaultStateMachineNotFoundError: There is more then one state machine in store. Indicate which state
    ...                machine should be used e.g.: ... sm_name=name-of-sm ...
    Run Keyword And Expect Error  ${msg}
    ...                           Add State  state=Fake Source State
    ...                                      on_update=On Update Fake Source State

    Update Context  state_invocation=${0}  sm_name=${second_sm_name}
    Run State Machine  sm_name=${second_sm_name}  start_from=Second Fake Source State  max_updates=10
    &{context}  Get Context  sm_name=${second_sm_name}
    Should Be Equal  ${context.get('state_invocation')}  ${6}

    &{context}  Get Context  sm_name=${first_sm_name}
    Should Be Equal  ${context.get('executed')}  ${NONE}

    @{simple_machine_states}=  Get State Machine States  sm_name=${first_sm_name}
    ${number_of_states}=  Get Length  ${simple_machine_states}
    Should Be Equal  ${number_of_states}  ${2}


*** Keywords ***
Fake Source State
    Update Context  executed=source

On Update Fake Source State
    Go To State  Fake Destination State

Fake Destination State
    &{new_context}=  Create Dictionary  executed=destination
    Set Context  ${new_context}

On Update Fake Destination State
    Stop State Machine

Second Fake Source State
    ${context}=  Get Context  sm_name=${second_sm_name}
    Update Context  state_invocation=${context['state_invocation'] + 1}  sm_name=${second_sm_name}

On Update Second Fake Source State
    Go To State  Second Fake Destination State  sm_name=${second_sm_name}

Second Fake Destination State
    No Operation

On Update Second Fake Destination State
    Go To State  Second Fake Source State  sm_name=${second_sm_name}
