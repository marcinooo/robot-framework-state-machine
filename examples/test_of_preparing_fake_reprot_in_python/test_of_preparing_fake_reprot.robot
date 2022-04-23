*** Settings ***
Library    StateMachineLibrary
Library    keywords.py


*** Test Cases ***
Prepare Report
    [Setup]    Prepare Report Setup
    ${sm_name}    Sm Name
    Go To State     state=get_battery_voltage    sm=${sm_name}
    Update State    sm=${sm_name}
    Update State    sm=${sm_name}
    Log To Console    OK
