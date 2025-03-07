# GSC-AVL-Script

V2.0 changes
- PyQT5 GUI
- Google Drive API Support

Installation
------------
### Audacity

Please download any Audacity Version 3.

- Link: https://www.audacityteam.org/

### PyQT5

- Link: https://pypi.org/project/PyQt5/


        pip3 install PyQT5

### send2Trash
- Link: https://pypi.org/project/Send2Trash/

        pip3 install send2trash

### Google API
- Link: https://developers.google.com/docs/api/quickstart/python

        pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Set Up
------
### Audacity
- Enable 'mod-script-pipe'
  
      Preferences -> Modules -> Enable 'mod-script-pipe'

### Google Cloud
Tutorial: https://www.youtube.com/watch?v=6bzzpda63H0
- Download client JSON file, rename it, add it to directory


### config.py
- Fill ``config.py`` file with local paths and Google Drive folder ids

      config = {
        'audacity': {
            'app_path': ''              # local path to 'Audacity' app
        },
        'local': {
            'save_path': ''             # local path to 'local_recordings' folder
        },
        'google': {
            'credentials_path': '',     # local path to 'credentials.json'
            'parent': ''                # Google Drive Parent folder ID
        },
        'good_stewards_service': {      # (https://drive.google.com/drive/folders/[ID found here])
            'music_folder': '',
            'sermon_folder': '',
            'misc_folder': ''
        },
        'cross_seeds_service': {
            'music_folder': '',
            'sermon_folder': '',
            'misc_folder': ''
        }
      }

### Usage
