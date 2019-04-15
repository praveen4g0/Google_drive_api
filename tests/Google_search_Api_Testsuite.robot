*** Settings ***
Resource               Common.robot
Test Template     Google Drive Api Search Testing
*** Variables ***
${query} =  name contains 'redbus'
${query1} =  name contains 'redbus' and mimeType contains 'image'
${Invalid_size} =  xyz
${Invalid_query} =  BluL̥e Jeans

*** Test Case ***
Positive_search    ${10}
Positive_search     ${5}
Invalid_pagination_search     ${-1}
Invalid_pagination_Search     ${1001}
Invalid_literal_Search     ${Invalid_size}


*** Keywords ***

Google Drive Api Search Testing
    [Arguments]  ${SIZE}
    Common.Set Driver service instance  ${SIZE}
    Common.Get List of Files From Drive provided pagination  ${SIZE}
    Common.Get List of Files From Drive Based on query paramter  ${query}


