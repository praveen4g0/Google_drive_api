import random
import logging
from locust import HttpLocust, TaskSet, task, seq_task
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class DownloadFilesBehavior(TaskSet):


    def on_start(self):


        """ on_start is called when a Locust start before any task is scheduled """
        log.debug('Application started ..... ')


    def on_stop(self):


        """ on_stop is called when the TaskSet is stopping """
        log.debug('Application Stopped ......')


    @seq_task(1)
    def download_file_to_local_drive(self):
        self.client.get("/downloadFileByApi/redbus.png/redbus.png")



class Google_Drive_Download_Api(HttpLocust):
    task_set = DownloadFilesBehavior
    min_wait = 5000
    max_wait = 9000

    """
    To see performance of Google_Drive_Download_Api in cmd 
    1. deploy module on port 9990

    2. deploy locust to monitor the performance and failure rate

    cmd 
    locust -f Performance/download_performance.py --host=http://localhost:9990

    check on 8090 port locust ui will be created to monitor performance of my api 
    """