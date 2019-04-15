from __future__ import print_function
import httplib2
# import atom.data
import gdata.data
import gdata.contacts.client
import gdata.contacts.data
from apiclient import discovery
from oauth2client import tools


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth


SCOPES = 'https://www.google.com/m8/feeds/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def getListOfContacts():

    gd_client = gdata.contacts.client.ContactsClient(source='Google_Contact_API')
    if gd_client is not None:
        PrintAllContacts(gd_client)


def PrintAllContacts(gd_client):
  feed = gd_client.GetContacts()
  for i, entry in enumerate(feed.entry):
    print('\n%s %s' % (i+1, entry.name.full_name.text))
    if entry.content:
      print('    %s' % (entry.content.text))
    # Display the primary email address for the contact.
    for email in entry.email:
      if email.primary and email.primary == 'true':
        print ('    %s' % (email.address))
    # Show the contact groups that this contact is a member of.
    for group in entry.group_membership_info:
      print ('    Member of group: %s' % (group.href))
    # Display extended properties.
    for extended_property in entry.extended_property:
      if extended_property.value:
        value = extended_property.value
      else:
        value = extended_property.GetXmlBlob()
      print ('    Extended Property - %s: %s' % (extended_property.name, value))



getListOfContacts()