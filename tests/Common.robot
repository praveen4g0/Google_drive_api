*** Settings ***
Library  ../tests/test_google_api.py



*** Keywords ***
Set Driver service instance
    [Tags]  Search
    [Arguments]  ${SIZE}
    set suite variable  ${SIZE}
    ${DRIVE} =  driver_service
    set suite variable  ${DRIVE}

Set Driver service instance Download
    [Tags]  Search
    ${DRIVE} =  driver_service
    set suite variable  ${DRIVE}

Get List of Files From Drive provided pagination
   [Tags]  Search
   [Arguments]  ${SIZE}
   ${FILES} =  get_all_files_provided_pagination  ${DRIVE}  ${SIZE}
   should not contain  ${FILES}  'Error'
   log  ${FILES}

Get List of Files From Drive Based on query paramter
    [Tags]  Search
    [Arguments]  ${querry}
    ${files} =  get list of file from drive based on query  ${DRIVE}  ${SIZE}  ${querry}
    should not contain  ${files}  'Error'
    log   ${files}

Download Single File to local drive after Search Api based on file name
   [Tags]  Download
   [Arguments]  ${file_name}  ${file_path}
   ${Result} =  download File after searching Api  ${DRIVE}  ${file_name}  ${file_path}
   should not contain  ${Result}  'Error'

Download Single Image File to local drive after Search Api
   [Tags]  Download
   [Arguments]  ${file_name}  ${file_path}
   ${Result} =  download File after searching Api  ${DRIVE}  ${file_name}  ${file_path}
   should not contain  ${Result}  'Error'

Google Drive Api Download Testing keyword
    [Tags]  Download
    [Arguments]  ${file_name}  ${file_path}
     ${DRIVE} =  driver_service
     set global variable  ${DRIVE}
     ${Result} =  download File after searching Api  ${DRIVE}  ${file_name}  ${file_path}
   should not contain  ${Result}  'Error'

Download Single Vedio File to local drive after Search Api
   [Tags]  Download
   [Arguments]  ${file_name}  ${file_path}
   ${Result} =  download File after searching Api  ${DRIVE}  ${file_name}  ${file_path}
   should not contain  ${Result}  'Error'

Download Single File to local drive after Search Api into another MimeType
   [Tags]  Download
   [Arguments]  ${file_name}  ${file_path}
   ${Result} =  download File after searching Api  ${DRIVE}  ${file_name}  ${file_path}
   should not contain  ${Result}  'Error'

Download Multiple File to local drive after Search Api
   [Tags]  Download
   [Arguments]  ${file_name}  ${file_path}
   download_multiple_files_after_searching_Api  ${DRIVE}  ${file_name}  ${file_path}