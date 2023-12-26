*** Settings ***
Library  StateMachineLibrary


*** Variables ***
${PRODUCT_A_STATE_MACHINE_NAME}  product-a-sm


*** Keywords ***
Product A Test Setup
    Create State Machine  ${PRODUCT_A_STATE_MACHINE_NAME}

    Add State  state=Initialize Product A Environment
    ...        on_update=On Update Initialize Product A Environment
    ...        sm_name=${PRODUCT_A_STATE_MACHINE_NAME}
    Add State  state=Start Product A Build
    ...        on_update=On Update Start Product A Build
    ...        sm_name=${PRODUCT_A_STATE_MACHINE_NAME}
    Add State  state=Check If Product A Is Ready
    ...        on_update=On Update Check If Product A Is Ready
    ...        sm_name=${PRODUCT_A_STATE_MACHINE_NAME}
    Add State  state=Prepare Final Report Of Building Product A
    ...        on_update=On Update Prepare Final Report Of Building Product A
    ...        sm_name=${PRODUCT_A_STATE_MACHINE_NAME}

Initialize Product A Environment
    Log To Console  Product A environment initialization

On Update Initialize Product A Environment
    Go To State  Start Product A Build  sm_name=${PRODUCT_A_STATE_MACHINE_NAME}

Start Product A Build
    Log To Console  Product A building

On Update Start Product A Build
    Go To State  Check If Product A Is Ready  sm_name=${PRODUCT_A_STATE_MACHINE_NAME}

Check If Product A Is Ready
    Log To Console  Checking if product A is ready
    ${status}=  Evaluate  random.choice(['ready', 'not-ready'])
    Update Context  status=${status}  sm_name=${PRODUCT_A_STATE_MACHINE_NAME}

On Update Check If Product A Is Ready
    &{context}=  Get Context  sm_name=${PRODUCT_A_STATE_MACHINE_NAME}
    IF  '${context['status']}' == 'ready'
        Go To State  Prepare Final Report Of Building Product A  sm_name=${PRODUCT_A_STATE_MACHINE_NAME}
    ELSE
        Go To State  Check If Product A Is Ready  sm_name=${PRODUCT_A_STATE_MACHINE_NAME}
    END

Prepare Final Report Of Building Product A
    Log To Console  Preparing Final Report of building product A

On Update Prepare Final Report Of Building Product A
    Stop State Machine  sm_name=${PRODUCT_A_STATE_MACHINE_NAME}
