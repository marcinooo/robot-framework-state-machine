*** Settings ***
Library    StateMachineLibrary
Library    keywords.py


*** Test Cases ***
Test Preparation of Report
    [Setup]    Prepare Report Setup
    ${sm_name}    Sm Name
    Go To State     state=Get Battery Voltage    sm=${sm_name}
    Update State    sm=${sm_name}
    Update State    sm=${sm_name}
    Log To Console    OK
