*** Settings ***
Resource  ./product_a_keywords.robot
Resource  ./product_b_keywords.robot


*** Test Cases ***
Test Correlation Of Building Two Products In The Same Time
    [Setup]  Run Keywords  Product A Test Setup  Product B Test Setup

    Go To State  Initialize Product A Environment  sm_name=${PRODUCT_A_STATE_MACHINE_NAME}
    Go To State  Initialize Product B Environment  sm_name=${PRODUCT_B_STATE_MACHINE_NAME}

    Repeat Keyword  20  Run Keywords    Update State  sm_name=${PRODUCT_A_STATE_MACHINE_NAME}  AND
    ...                                 Update State  sm_name=${PRODUCT_B_STATE_MACHINE_NAME}
