import os
import unittest

from googleapiclient.errors import InvalidChunkSizeError
from googleapiclient.http import MediaFileUpload, MediaInMemoryUpload, MediaUpload

DATA_DIR = os.path.join(os.path.dirname(__file__), 'resources')


def datafile(filename):
  return os.path.join(DATA_DIR, filename)

def _postproc_none(*kwargs):
  pass

class TestMediaUpload(unittest.TestCase):

  def test_media_file_upload_mimetype_detection(self):
    upload = MediaFileUpload(datafile('redbus.png'))
    self.assertEqual('image/png', upload.mimetype())

    # upload = MediaFileUpload(datafile('empty'))
    # self.assertEqual('application/octet-stream', upload.mimetype())

  def test_media_file_upload_to_from_json(self):
    upload = MediaFileUpload(
        datafile('redbus.png'), chunksize=500, resumable=True)
    self.assertEqual('image/png', upload.mimetype())
    self.assertEqual(7557, upload.size())
    self.assertEqual(True, upload.resumable())
    self.assertEqual(500, upload.chunksize())
    self.assertEqual(b'PNG', upload.getbytes(1, 3))

    json = upload.to_json()
    new_upload = MediaUpload.new_from_json(json)

    self.assertEqual('image/png', new_upload.mimetype())
    self.assertEqual(7557, new_upload.size())
    self.assertEqual(True, new_upload.resumable())
    self.assertEqual(500, new_upload.chunksize())
    self.assertEqual(b'PNG', new_upload.getbytes(1, 3))

  def test_media_file_upload_raises_on_invalid_chunksize(self):

      """
        raise InvalidChunkSizeError()
        googleapiclient.errors.InvalidChunkSizeError
      :return:
      """
      self.assertRaises(InvalidChunkSizeError, MediaFileUpload,
         datafile('redbus.png'), mimetype='image/png', chunksize=-2,
        resumable=True)


  def test_media_inmemory_upload(self):
    media = MediaInMemoryUpload(b'abcdef', mimetype='text/plain', chunksize=10,
                                resumable=True)
    self.assertEqual('text/plain', media.mimetype())
    self.assertEqual(10, media.chunksize())
    self.assertTrue(media.resumable())
    self.assertEqual(b'bc', media.getbytes(1, 2))
    self.assertEqual(6, media.size())
