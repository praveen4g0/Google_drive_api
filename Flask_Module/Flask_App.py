from __future__ import print_function
import httplib2
import os, io

from werkzeug.exceptions import abort

import Utilities.csv_utility as cs
from apiclient import discovery
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
# from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import logging

logger = logging.getLogger(__name__)

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
import os
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify, render_template

from flask import Blueprint, jsonify
errors = Blueprint('errors', __name__)
cur_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(cur_path, r"..\Logs\html_logs")
UPLOAD_FOLDER = path
ALLOWED_EXTENSIONS = set(['log', 'pdf', 'png', 'jpg', 'jpeg', 'mp4','html'])

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.getCredentials()
http = credentials.authorize(httplib2.Http())
drive_service= discovery.build('drive', 'v3', http=http)

@app.route("/",methods=['GET'])
def hello():
    return jsonify({'Message':"it's working" })

@app.route("/getAllFilesDetails/<int:size>",methods=['GET'])
def listFiles(size):
    lst=[]
    try:
        results = drive_service.files().list(
            pageSize=size, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])
        if not items:
            logger.error('No Files found ... process terminating')
            os._exit(0)
        else:
            for item in items:
                print('{} : {} : {} \n'.format(item['name'], item['id'], item['mimeType']))
            # cs.write_to_csv(items)

        return jsonify({'Items': items})
    except Exception as e:
        raise InvalidUsage(e, status_code=404)

def uploadFile(filename, filepath, mimetype):
        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath,
                            mimetype=mimetype)
        file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        print('File ID: %s' % file.get('id'))

@app.route("/downloadFile/<string:filename>/<string:filepath>",methods=['GET'])
def downloadFile(filename, filepath):
    try:
        file_id = cs.read_csv_get_Fileid(filename)[0]
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        return jsonify({'Message':'Downloaded successfully'})
    except Exception as e:
        raise InvalidUsage(e, status_code=404)


@app.route("/downloadFileByApi/<string:file_name>/<string:filepath>",methods=['GET'])
def downloadFile_after_searching_Api(file_name, filepath):
     try:
        file_id = searchFile(10, f"name contains '{file_name}'")[0]['id']
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        return jsonify({'Message':'Downloaded successfully'})
     except Exception as e:
        raise InvalidUsage(e, status_code=404)

@app.route("/downloadMultipleFiles/<string:file_name>/<string:filepath>",methods=['GET'])
def downloadAllFile_after_searching_Api(file_name, filepath):
        files =searchFile(5, f"name contains '{file_name}'")
        for file in files:
            request = drive_service.files().get_media(fileId=file['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                try:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))
                except Exception as e:
                    pass
            with io.open(filepath, 'wb') as f:
                fh.seek(0)
                f.write(fh.read())


def createFolder(name):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
         }
        file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
        print('Folder ID: %s' % file.get('id'))

@app.route("/getFilesOnQueryParam/<int:size>/<string:query>",methods=['GET'])
def searchFile(size, query):
      try:
        results = drive_service.files().list(
            pageSize=size, fields="nextPageToken, files(id, name, kind, mimeType)", q=f"name contains '{query}'").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
         print('Files:')
         for item in items:
                print(item)
                print('{0} ({1})'.format(item['name'], item['id']))

         return jsonify({"Items":items})
      except Exception as e:
        raise InvalidUsage(e, status_code=404)


@errors.app_errorhandler(Exception)
def handle_error(error):
    message = [str(x) for x in error.args]
    status_code = error.status_code
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message,
            'status': status_code
        }
    }
    return jsonify(response), status_code


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

@app.route('/500')
def error():
		abort(500)


if __name__ == "__main__":
    app.run(debug=True,port=9990)
