from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']

def create_public_link_for_fileid(service,fileId):
    """Creates public link for fileId in Google Drive
    Should know fileId
    Should have service=build('drive', 'v3', credentials=creds)
    Credentials should have write access to Google Drive
    """
    new_permission = {
      'allowFileDiscovery': False,
      'type': 'anyone',
      'role': 'reader'
    }
    result = service.permissions().create(
            fileId=fileId, body=new_permission).execute()
#    print(result)

def create_service():
    """
    Creates connection the Drive v3 API.
    To aquire access to Google Account 
    Requires: credentials.json
    Then in web browser the access is granted by user.
    Credentials are stored at: token.pickle
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def find_dir_by_name_get_fileId(service, dirname):
    """
    If the only one dir with dirname found in Google Drive,
    it's fileId is returned. Otherwise returns None
    Should have service=build('drive', 'v3', credentials=creds)
    """

    query = "name = '{}'\n".format(dirname)
    query += "and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(
        q=query, 
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print("No dir with name '{0}' found.".format(dirname))
        return None
    else:
        if (len(items) > 1):
            print("Multiple dirs with name '{0}' were found:".format(dirname))
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
            return None
        else:
            print("Dir with name '{0}' found:".format(dirname))
            print(u'{0} ({1})'.format(items[0]['name'], items[0]['id']))
            return items[0]['id']
        


    
def create_and_print_webLink_for_every_subdir(service, fileId, createLink, createFeedback):
    """
    Creates and prints public webLink
    for each file or directory with parent "fileId"
    no more than 1000 of those files/dirs inside the main dir.
    Create locally dir with same name and subdirs with same names,
    putting files into it with corresponding links
    """
    query = "'{}' in parents\n".format(fileId)
    query += "and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(
        q=query, 
        pageSize=1000, fields="nextPageToken, files(id, name, webViewLink)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            if createLink:
                create_public_link_for_fileid(service,item['id'])

            if createFeedback:
                os.mkdir(item['name'])
                with open("{0}/feedback.txt".format(item['name']),'w') as f:
                    f.write(item.get('webViewLink','none'))

            print(u'{0} ({1}) {2}'.format(item['name'], item['id'], item.get('webViewLink','none')))
    
def main():
    """Work with students papers feedbacks in Google Drive,
    creating each student weblink to his/her own feedback,
    so no student can access feedbacks of other students.
    """
    service = create_service()
    
    
    folderName = "multi_feedback_test-3_778"
    createLink = False  # links already created in previous run
    createFeedback = True  # feedbacks already created in previous run

    folderId = find_dir_by_name_get_fileId(service, folderName)
    if (folderId):
        if createFeedback:
            os.mkdir(folderName)
            os.chdir(folderName)
            print("Feedback created in dir: {}".format(os.getcwd()))
        create_and_print_webLink_for_every_subdir(service, folderId, createLink, createFeedback)
        
if __name__ == '__main__':
    main()