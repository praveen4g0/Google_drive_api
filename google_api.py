from __future__ import print_function

import unittest

import httplib2
import os, io


import Utilities.csv_utility as cs
from apiclient import discovery
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaUpload, MediaInMemoryUpload, build_http, \
    HttpRequest

import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import auth

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json

class google_drive_api:
    drive_service=None
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'Drive API Python Quickstart'
        authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
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


    def uploadFile(self,filename, filepath, mimetype,chunksize):
        file_metadata = {'name': filename}

        media = MediaFileUpload(filepath,
                            mimetype=mimetype,chunksize=chunksize)
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




# uploadFile('unnamed.jpg','unnamed.jpg','image/jpeg')
# downloadFile('Blue Jeans','BlueJeans.pdf')
# createFolder('Google')
# searchFile(10,"name contains 'redbus' and mimeType contains 'image'")
# downloadFile_after_searching_Api('BluL̥e Jeans','BlueJeans.pdf')
# listFiles(10)

