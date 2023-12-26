*** Settings ***
Library  StateMachineLibrary


*** Variables ***
${PRODUCT_B_STATE_MACHINE_NAME}  product-b-sm


*** Keywords ***
Product B Test Setup
    Create State Machine  ${PRODUCT_B_STATE_MACHINE_NAME}

    Add State  state=Initialize Product B Environment
    ...        on_update=On Update Initialize Product B Environment
    ...        sm_name=${PRODUCT_B_STATE_MACHINE_NAME}
    Add State  state=Start Product B Build
    ...        on_update=On Update Start Product B Build
    ...        sm_name=${PRODUCT_B_STATE_MACHINE_NAME}
    Add State  state=Check If Product B Is Ready
    ...        on_update=On Update Check If Product b Is Ready
    ...        sm_name=${PRODUCT_B_STATE_MACHINE_NAME}
    Add State  state=Prepare Final Report Of Building Product B
    ...        on_update=On Update Prepare Final Report Of Building Product B
    ...        sm_name=${PRODUCT_B_STATE_MACHINE_NAME}

Initialize Product B Environment
    Log To Console  Product B environment initialization

On Update Initialize Product B Environment
    Go To State  Start Product B Build  sm_name=${PRODUCT_B_STATE_MACHINE_NAME}

Start Product B Build
    Log To Console  Product B building

On Update Start Product B Build
    Go To State  Check If Product B Is Ready  sm_name=${PRODUCT_B_STATE_MACHINE_NAME}

Check If Product B Is Ready
    Log To Console  Checking if product B is ready
    ${status}=  Evaluate  random.choice(['ready', 'not-ready'])
    Update Context  status=${status}  sm_name=${PRODUCT_B_STATE_MACHINE_NAME}

On Update Check If Product B Is Ready
    &{context}=  Get Context  sm_name=${PRODUCT_B_STATE_MACHINE_NAME}
    IF  '${context['status']}' == 'ready'
        Go To State  Prepare Final Report Of Building Product B  sm_name=${PRODUCT_B_STATE_MACHINE_NAME}
    ELSE
        Go To State  Check If Product B Is Ready  sm_name=${PRODUCT_B_STATE_MACHINE_NAME}
    END

Prepare Final Report Of Building Product B
    Log To Console  Preparing Final Report of building product B

On Update Prepare Final Report Of Building Product B
    Stop State Machine  sm_name=${PRODUCT_B_STATE_MACHINE_NAME}
