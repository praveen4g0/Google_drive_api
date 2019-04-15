**Project Title**
The Drive platform gives you a group of APIs along with client libraries, language-specific examples, and documentation to help you develop apps that integrate with Drive.

The core functionality of Drive apps is to search ,download and upload files in Google Drive. However, the Drive platform provides a lot more than just storage. This page describes some of that functionality and points you to resources for building it into your app.

**Getting Started**
1. Unit Test Cases
2. Robot Framework (Functional Test cases)
3. Application API's Developed using flask module (For Performance)
4. Performance Testing using locust

**Prerequisites**
_Modules:_
GoggleDriveApiClient modules (To establish connection to Google Api from your Application)
Flask module (To Expose/Deploy API's of your Application making use of Google Api's)
locust module (To perform performance test)
pytest (To perform unit testing)
Robot Framework (To perform functional test)
 

**Tests Performed**
All unit/Function tests under tests directory

Unit Test:
directory - tests/test_*, TestRunner

Functional Test:
directory - tests/Google_*.robot

Performance Test:
directory - Performance/*_performance.py

Reports of Functional Test:
directory - reports/*



**_How to run Unit tests_**
open cmd
cd current_working_Directory/tests/TestRunner*.py (Runs test_auth,test_media_upload tests)

or use py_spec plugin to run unit test cases

**Available features**
Format output to look like specification.
Group tests by classes and files
Failed, passed and skipped are marked and colored.
Remove test_ and underscores for every test.

**Output example**
py.test --spec

tests/test_results/test_as_class.py::TestResults
    [SKIP]  Some method return none
    [FAIL]  Some method returns false
    [PASS]  Some method returns true

tests/test_results/test_as_functions.py
    [PASS]  Some method returns true
    [FAIL]  Some method returns false
    [SKIP]  Some method return none
    
**Install**
pip install pytest-spec


test_google_Api.py has all unit test cases 

all Downloaded files will be under resources section 

**Functionla Test Cases**    

Directory tests/Google_*.robot

**Available Features**
Format output to look like HTML.
Group tests by suites and classes
Failed, passed and skipped are marked and colored.
neat looking Report will be generated under reports directory

**Output example**

pybot -d <reports directory> <tests/RobotFile directory>

-d destination in which reports to be stored

Eg: pybot -d reports tests/Google_search_Api.robot

**Reports**
Reports will be reports directory open report.html to view last run reports 

**Procedure to do performance testing**
Flask_Module - to Deploy/ Expose my application APi's to public
Performance - Locust module to do performance test on exposed api's


 """
 To see performance of getFilesBehaviour in cmd 
 1. deploy module on port 9990
 
 2. deploy locust to monitor the performance and failure rate with percentiles
 
 cmd 
 locust -f Performance/search_performance.py --host=http://localhost:9990
 
 check on 8090 port locust ui will be created to monitor performance of my api 
 """
 
 
**Prerequisites**
Need to deploy our API's into 9990 port to test its performance

1. we can run directly .py file  Flask_Module/Flask_App.py which will deploy your instance into 9990 port


_**How to verify flask module is working or not**_

 search API:
 
 http://localhost:9990/getAllFilesDetails/<paginationsize:int>
 http://localhost:9990/getFilesOnQueryParam/<paginationsize:int>/<query:string>
 http://localhost:9990/downloadFileByApi/<query:int>/<path_to_stroe_locally:string>
 
 Eg:
 search Api: http://localhost:9990/getAllFilesDetails/10
 search Api: http://localhost:9990/getFilesOnQueryParam/10/redbus
 Download Api: http://localhost:9990/downloadFileByApi/Blue Jeans/Bluejeans.pdf
 check in download module if download is successfull
 
 


2. you can try to deploy locust  module on default port of 8089
  monitor performance of Application on 8089 port
  
  