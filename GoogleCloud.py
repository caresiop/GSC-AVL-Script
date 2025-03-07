import os

from config import config
from googleapiclient.http import MediaFileUpload
from google_apis import create_service

class GoogleCloud():
    def __init__(self):
        # Google API service startup
        # Tutorial: https://www.youtube.com/watch?v=6bzzpda63H0
        # Documentation: https://developers.google.com/docs/api/quickstart/python (Used some of this)
        
        self.CLIENT_SECRET_FILE = config['google']['credentials_path']
        self.API_NAME = 'drive'
        self.API_VERSION = 'v3'
        self.SCOPES = ['https://www.googleapis.com/auth/drive']

        self.service = create_service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)

        self.parent_id = config['google']['parent']

        self.sermon_link = []
        self.music_link = []
        self.misc_link = []

        self.cross_seeds_flag = False


    # Upload files onto Google Drive
    def upload_files(self):
        # Tutorial: https://youtu.be/cCKPjW5JwKo?feature=shared
        # Consideration: https://github.com/googleapis/google-api-python-client/blob/main/docs/media.md#resumable-media-chunked-upload
        
        self.file_names = os.listdir(config['local']['save_path'])
        mime_type = 'audio/mpeg'

        for file_name in self.file_names:
            if ".mp3" in file_name:
                file_metadata = {
                    'name': file_name,
                    'parents': [self.parent_id]
                }

                media = MediaFileUpload(config['local']['save_path'] + '/{0}'.format(file_name), mimetype = mime_type)

                self.service.files().create(
                    body = file_metadata,
                    media_body = media,
                    fields = 'id'
                ).execute()


    # List files & folders on Google Drive
    def list_contents(self):
        # Tutorial: https://youtu.be/kFR-O8BHIH4?feature=shared
        # Mime Types: https://learndataanalysis.org/commonly-used-mime-types/
        # Meta data: https://developers.google.com/drive/api/reference/rest/v3/files

        query = f"parents = '{self.parent_id}' and mimeType = 'audio/mpeg' and trashed = false"
        response = self.service.files().list(q = query).execute()
        self.files = response.get('files')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = self.service.files().list(q = query, pageToken = nextPageToken).execute()
            self.files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')


    # Helper to move files to their respective directories
    def move_file_to_folder(self, file_id, folder_id):
        # https://developers.google.com/drive/api/guides/folder#python_2

        file = self.service.files().get(fileId=file_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents"))
        # Move the file to the new folder
        file = (
            self.service.files()
            .update(
                fileId=file_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields="id, parents",
            )
            .execute()
        )


    # Share Links
    def share_links(self):
        # Tutorial: https://youtu.be/eO-7RIMTjOA?feature=shared
        request_body = {
        'role': 'reader',
        'type': 'anyone'
        }

        service = config['good_stewards_service']
        if self.cross_seeds_flag:
            service = config['cross_seeds_service']

        for f in self.files:
            name = f['name']
            id = f['id']
            time = int(f['name'][11:19].replace('.', ''))

            self.service.permissions().create(
                fileId = id,
                body = request_body
            ).execute()

            link = self.service.files().get(
                fileId = id,
                fields = 'webViewLink'
            ).execute()

            if 'Sermon' in name or 'sermon' in name:
                self.sermon_link.append({'name': name, 'id': id, 'time': time, 'link': link['webViewLink']})
                self.move_file_to_folder(id, service['sermon_folder'])
            elif 'Music' in name or 'music' in name:
                self.music_link.append({'name': name, 'id': id, 'time': time, 'link': link['webViewLink']})
                self.move_file_to_folder(id, service['music_folder'])
            else:
                self.misc_link.append({'name': name, 'id': id, 'time': time, 'link': link['webViewLink']})
                self.move_file_to_folder(id, service['misc_folder'])


    def get_music_links(self):
        return self.music_link
    

    def get_sermon_links(self):
        return self.sermon_link
    

    def get_misc_links(self):
        return self.misc_link
    

    def sort_links(self):
        def helper(file):
            return file['time']
        
        self.music_link.sort(key=helper)
        self.sermon_link.sort(key=helper)
        self.misc_link.sort(key=helper)
    

    def clear_links(self):
        self.music_link = []
        self.sermon_link = []
        self.misc_link = []
    

    def cross_seeds(self, flag):
        self.cross_seeds_flag = flag

    
    def exec(self):
        self.upload_files()
        self.list_contents()
        self.share_links()
        self.sort_links()
