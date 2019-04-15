import logging
from locust import HttpLocust, TaskSet, task, seq_task
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)




class GetFilesBehavior(TaskSet):


    def on_start(self):


        """ on_start is called when a Locust start before any task is scheduled """
        log.debug('Application started ..... ')


    def on_stop(self):


        """ on_stop is called when the TaskSet is stopping """
        log.debug('Application Stopped ......')



    @task(2)
    def get_files_on_query_param(self):
        """
        list down files based on query parameter from google drive provided pagination atmost size of files displayed would be pagination
        :return:
        """
        self.client.get("/getFilesOnQueryParam/10/redbus")

    @task(1)
    def get_all_files_specified_pagination(self):
        """
        list down all available Files in Google Drive /10 specifies pagination how many files you were expecting at each hit AllFileData.csv will be created at run time
        :return:
        """
        self.client.get("/getAllFilesDetails/10")





class Google_Drive_search_Api(HttpLocust):
 task_set = GetFilesBehavior
 min_wait = 5000
 max_wait = 9000


 """
 To see performance of getFilesBehaviour in cmd 
 1. deploy module on port 9990
 
 2. deploy locust to monitor the performance and failure rate
 
 cmd 
 locust -f Performance/search_performance.py --host=http://localhost:9990
 
 check on 8090 port locust ui will be created to monitor performance of my api 
 """


