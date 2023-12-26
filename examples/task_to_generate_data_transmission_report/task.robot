*** Settings ***
Library    StateMachineLibrary
Library    ./keywords.py


*** Variables ***
${data_transmission_test_line_log_path}  ${CURDIR}${/}data_transmission_test_line.json
${data_transmission_log_path}            ${CURDIR}${/}data_transmission.csv
${final_report_path}                     ${OUTPUT DIR}${/}data-transmission-report.html


*** Tasks ***
Prepare Data Transmission Report
    [Setup]  Task Setup
    Run State Machine  start_from=Parse test line info log
