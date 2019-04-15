from __future__ import print_function

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import unittest

import httplib2
import os, io


import Utilities.csv_utility as cs
from apiclient import discovery
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

import logging



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
flags=True

class auth:
    def __init__(self,SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME):
        self.SCOPES = SCOPES
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.APPLICATION_NAME = APPLICATION_NAME
    def getCredentials(self):
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Returns:
            Credentials, the obtained credential.
        """
        cwd_dir = os.getcwd()
        credential_dir = os.path.join(cwd_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'google-drive-client_secret.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            logger.debug('Storing credentials to ' + credential_path)
        return credentials


def driver_service():
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Drive API Python Quickstart'
    authInst = auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
    credentials = authInst.getCredentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)
    return drive_service


def get_all_files_provided_pagination(drive_service,size):
    res={}
    try:
        results = drive_service.files().list(
            pageSize=size, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])
        if not items:
            res = {'Error': 'No Files found ... process terminating'}
            logger.debug('No Files found ... process terminating')
            os._exit(0)
        else:
            for item in items:
                logger.debug('{} : {} : {}'.format(item['name'], item['id'], item['mimeType']))
            res = {'Message': items}
            cs.write_to_csv(items)
            return res
    except Exception as e:
        raise e


def upload_file_to_drive(drive_service,filename, filepath, mimetype):
        file_metadata = {'name': filename}

        cwd_dir = os.getcwd()
        filepath = os.path.join(cwd_dir, filepath)
        try:
            media = MediaFileUpload(filepath,
                            mimetype=mimetype)
        except Exception as e:
            logger.error(e)
        file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        logger.debug('File ID: %s' % file.get('id'))

def download_file_from_drive_with_filename(drive_service,file_name, filepath):
        file_id = cs.read_csv_get_Fileid(file_name)[0]
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logger.debug("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())

def download_File_after_searching_Api(drive_service,file_name, filepath):
        logger.debug(driver_service)

        file_id = get_list_of_file_from_drive_based_on_query(drive_service, 5, f"name contains '{file_name}'")[0]['id']
        res ={}
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        try:
            while done is False:
                status, done = downloader.next_chunk()
                logger.debug("Download %d%%." % int(status.progress() * 100))
            with io.open(filepath, 'wb') as f:
                fh.seek(0)
                f.write(fh.read())
            res={'Message':'Downloaded to local Drive Sucessfully'}
        except Exception as e:
             res={'Error':f'Error in Download {e}'}
        return res
def download_multiple_files_after_searching_Api(drive_service,file_name, filepath):
        file_id = get_list_of_file_from_drive_based_on_query(drive_service,5, f"name contains '{file_name}'")
        counter = 0
        for file in file_id:
            request = drive_service.files().get_media(fileId=file['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False

            while done is False:
                try:
                        status, done = downloader.next_chunk()
                        print("Download %d%%." % int(status.progress() * 100))
                        logger.debug("Download %d%%." % int(status.progress() * 100))
                except Exception as e:
                    counter+=1
                    logger.error(" Unable to download file {}".format(e))
                    done=True
            with io.open(filepath, 'wb') as f:
                fh.seek(0)
                f.write(fh.read())
        if counter>0:
            raise Exception(f'{counter} Files Didnt get Downloaded ')
            os._exit(0)

def create_Folder_into_drive(drive_service,name):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
         }
        file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()

        logger.debug('Folder ID: %s' % file.get('id'))


def get_list_of_file_from_drive_based_on_query(drive_service,size, query):
        logger.debug(drive_service,size,query)
        res={}
        try:
            results = drive_service.files().list(
                pageSize=size, fields="nextPageToken, files(id, name, kind, mimeType)", q=query).execute()
        except Exception as e:
            logger.error(f'Error occured due to{ e} valid parameters size: int/float 10/10.5 not String "10.5" and querry valid string ')
            raise Exception(e)

        items = results.get('files', [])

        if not items:
            logger.debug('No files found.')
            res={'Error':items}
        else:
         logger.debug('Files:')
         for item in items:
             logger.debug('{0} ({1})'.format(item['name'], item['id']))
         res={'Message':items}
        return items





class google_drive_api:
    drive_service=None
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'Drive API Python Quickstart'
        authInst = auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
        credentials = authInst.getCredentials()
        http = credentials.authorize(httplib2.Http())
        global drive_service
        drive_service= discovery.build('drive', 'v3', http=http)



    def listFiles(self,size):
        try:
            results = drive_service.files().list(
                pageSize=size, fields="nextPageToken, files(id, name, mimeType)").execute()
            res = {}
            items = results.get('files', [])
            if not items:
                res = {'Error': 'No Files found ... process terminating'}
                logger.debug('No Files found ... process terminating')
                os._exit(0)
            else:
                for item in items:
                    logger.debug('{} : {} : {}'.format(item['name'], item['id'], item['mimeType']))
                res = {'Message': items}
                cs.write_to_csv(items)
                return res
        except Exception as e:
           raise e


    def uploadFile(self,filename, filepath, mimetype):
        file_metadata = {'name': filename}

        media = MediaFileUpload(filepath,
                            mimetype=mimetype)
        file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        logger.debug('File ID: %s' % file.get('id'))


    def downloadFile(self,file_name, filepath):
        file_id = cs.read_csv_get_Fileid(file_name)[0]
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logger.debug("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())


    def downloadFile_after_searching_Api(self,file_name, filepath):
        file_id = self.searchFile(10, f"name contains '{file_name}'")[0]['id']
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logger.debug("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())


    def downloadAllFile_after_searching_Api(self,file_name, filepath):
        file_id = self.searchFile(5, f"name contains '{file_name}'")
        counter = 0
        for file in file_id:
            request = drive_service.files().get_media(fileId=file['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False

            while done is False:
                try:
                        status, done = downloader.next_chunk()
                        print("Download %d%%." % int(status.progress() * 100))
                        logger.debug("Download %d%%." % int(status.progress() * 100))
                except Exception as e:
                    counter+=1
                    logger.error(" Unable to download file {}".format(e))
                    done=True
            with io.open(filepath, 'wb') as f:
                fh.seek(0)
                f.write(fh.read())
        if counter>0:
            raise Exception(f'{counter} Files Didnt get Downloaded ')
            os._exit(0)

    def createFolder(self,name):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
         }
        file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()

        logger.debug('Folder ID: %s' % file.get('id'))


    def searchFile(self,size, query):
        try:
            results = drive_service.files().list(
                pageSize=size, fields="nextPageToken, files(id, name, kind, mimeType)", q=query).execute()
        except Exception as e:
            logger.error(f'Error occured due to{ e} valid parameters size: int/float 10/10.5 not String "10.5" and querry valid string ')
            raise Exception(e)

        items = results.get('files', [])
        if not items:
            logger.debug('No files found.')
        else:
         logger.debug('Files:')
         for item in items:
             logger.debug('{0} ({1})'.format(item['name'], item['id']))
        return items




# upload_Folder_into_drive('reports','unnamed.jpg','image/jpeg')
# downloadFile('Blue Jeans','BlueJeans.pdf')

# searchFile(10,"name contains 'redbus' and mimeType contains 'image'")
# downloadFile_after_searching_Api('BluL̥e Jeans','BlueJeans.pdf')
# listFiles(10)


class SimpleTest(unittest.TestCase):
    gdinst=None


    def setUp(self):
        global gdinst
        gdinst=google_drive_api()


    def test_getAllFiles_positive(self):
        res=gdinst.listFiles(10)
        if str(res).__contains__('Message'):
            self.assertTrue(True)
        elif  str(res).__contains__('Error'):
            self.assertFalse()

    def test_getAllFiles_codeBreak(self):
      """
               code will break on any value beyond [1-1000]
      """
      res=gdinst.listFiles(-1)
      if str(res).__contains__('Message'):
            self.assertTrue(True)
      elif  str(res).__contains__('Error'):
            self.assertFalse()

    def test_getAllFiles_unexpectedBhevaiour(self):
        """
        ValueError: invalid literal for int() with base 10: '13.0'|'15.0' etc
        for 13 its successful
        ValueError: invalid literal for int() with base 10: '13.0'
        :return:
        """
        res = gdinst.listFiles("15.0")
        if str(res).__contains__('Message'):
            self.assertTrue(True)
        elif str(res).__contains__('Error'):
            self.assertFalse()

    def test_getAllFiles_FloatPagination(self):

        """
        takes floor value of float to get pagination
        :return:
        """
        res = gdinst.listFiles(7.9)
        if str(res).__contains__('Message'):
            self.assertTrue(True)
        elif str(res).__contains__('Error'):
            self.assertFalse()


    def test_download_file_PNG(self):
        res = gdinst.downloadFile_after_searching_Api('redbus.png', 'redbus.png')
        if str(res).__contains__('Message'):
            self.assertTrue(True)
        elif str(res).__contains__('Error'):
            self.assertFalse()

    def test_download_file_vedio(self):
        res = gdinst.downloadFile_after_searching_Api('VID','vedio.mp4')
        if str(res).__contains__('Message'):
            self.assertTrue(True)
        elif str(res).__contains__('Error'):
            self.assertFalse()


    def test_download_file_into_different_mimeType(self):
        """
         # res = gdinst.downloadFile_after_searching_Api('redbus.png', 'redbus.docs')
        # res = gdinst.downloadFile_after_searching_Api('redbus.png', 'redbus.mp4')
        #  res = gdinst.downloadFile_after_searching_Api('redbus.png', 'redbus.json')
        works Perfectly fine
        # res = gdinst.downloadFile_after_searching_Api('redbus','redbus.pdf') will get forbidden error as we try to download docs file into pdf which is not supported format

        :return:
        """
        res = gdinst.downloadFile_after_searching_Api('redbus','redbus.pdf')
        if str(res).__contains__('Message'):
                self.assertTrue(True)
        elif str(res).__contains__('Error'):
                self.assertFalse()

    def test_download_multiple_files_into_mimeType(self):
        """
        when we try to download multiple files with querry parameter which has different file formates and mimeType doesnt matches it throws forbidden error
        some docs cannot be converted to pdf
        :return:
        """
        res = gdinst.downloadAllFile_after_searching_Api('redbus', 'redbus.pdf')
        if str(res).__contains__('Message'):
            self.assertTrue(True)
        elif str(res).__contains__('Error'):
            self.assertFalse()


    def test_download_single_File_with_invalid_querryParam(self):
        """
        when we try to download a file based on file name with invalid querryparam  Code will break
        :return:
        """
        res = gdinst.downloadFile_after_searching_Api('Blue Jeans', 'BlueJeans.pdf')
        if str(res).__contains__('Message'):
                self.assertTrue(True)
        elif str(res).__contains__('Error'):
                self.assertFalse()

    def test_search_files_based_on_querry_param(self):
            res = gdinst.searchFile("10", "name contains 'redbus' and mimeType contains 'image'")
            if str(res).__contains__('Message'):
                self.assertTrue(True)
            elif str(res).__contains__('Error'):
                self.assertFalse()

    def test_search_files_based_on_inccorect_Querry_param(self):
        res=gdinst.searchFile(10,"BluL̥e Jeans")
        if str(res).__contains__('Message'):
                    self.assertTrue(True)
        elif str(res).__contains__('Error'):
                    self.assertFalse()

    def test_codeBreak_throwup_with_invalid_listFiles(self):
        self.assertRaises(Exception,gdinst.listFiles,-3)

    def test_codeBreak_with_invalid_size(self):
        self.assertRaises(Exception, gdinst.listFiles, "10.0")

    def test_codeBreak_with_invalid_size(self):
        self.assertRaises(Exception,gdinst.listFiles,"xyz")


    def tearDown(self):
         pass



if __name__ == '__main__':
     unittest.main()


