*** Settings ***
Resource               Common.robot

*** Variables ***
${query} =  Blue Jeans
${file_path} =  resources/BlueJeans.pdf
${query1} =  redbus.png
${file_path1} =  resources/redbus.png
${query2} =  VID
${file_path2} =  resources/vedio.mp4
${query4} =  redbus
${mimeType} =  resources/redbus.pdf


*** Test Case ***

Google Drive Api Driver Servce Instance
    [Tags]  Download
    Common.Set Driver service instance Download

Google Drive Api Download Single File Test
    [Tags]  Download
    Common.Download Single File to local drive after Search Api based on file name  ${query}  ${file_path}

Google Drive Api Download same File multiple times Test
    [Tags]  Download
    Common.Download Single File to local drive after Search Api based on file name  ${query}  ${file_path}

Google Drive Api Download image file
    [Tags]  Download
    Common.Download Single File to local drive after Search Api based on file name  ${query1}  ${file_path1}
Google Drive Api Download vedio file
    [Tags]  Download
    Common.Download Single File to local drive after Search Api based on file name  ${query2}  ${file_path2}
Google Drive Api Download file into different mimeType
     [Tags]  Download
     Common.Download Single File to local drive after Search Api into another MimeType  ${query}  resources/redbus.docs
Google Drive Api Multiple File to local drive
    [Tags]  Download
    Common.Download Multiple File to local drive after Search Api   ${query4}   ${mimeType}