# GSC-AVL-Script

**v2.0 changes**
- ``PyQT5`` GUI
- ``Google Drive API`` Support
- ``Cross Seeds`` session added
- App text editor to log and view actions

## Installation

### ``Audacity``

Please download any ``Audacity`` **v3**.

- *https://www.audacityteam.org/*

---

### ``PyQT5``

- *https://pypi.org/project/PyQt5/*

      pip3 install PyQT5

---

### ``send2Trash``
- *https://pypi.org/project/Send2Trash/*

      pip3 install send2trash

---

### ``Google API``
- *https://developers.google.com/docs/api/quickstart/python*

      pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

---

Set Up
------
### ``Audacity``
- Enable ``'mod-script-pipe'``
  
      Preferences -> Modules -> Enable 'mod-script-pipe'

---

### ``Google Cloud``
Tutorial: *https://www.youtube.com/watch?v=6bzzpda63H0*
- *https://console.cloud.google.com*
- Download client ``JSON`` file, rename it, and add it to local directory
- Add a new ``Test User`` with a usable ``Gmail`` account

      Sidebar -> APIs & Services -> OAuth consent screen -> Audience -> Test Users

---

### ``config.py``
- Fill ``config.py`` file with local paths and with Google Drive folder ids

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

---

### Test Folders

- Parent folder: *https://drive.google.com/drive/folders/1Kj4ezQYKGRUn4QKl8rUQtyuo3JlIi4Pz?usp=sharing*

- 'GSC' folder: *https://drive.google.com/drive/folders/1s061yboiwKgqWVvSW0oYhwxz21ejG7O7?usp=sharing*

- 'Cross Seeds' folder: *https://drive.google.com/drive/folders/12K29Zq0RGmT2t0xM9BB51sb8blhlMpwE?usp=sharing*

---

## Usage

      python3 GSC_Recording_Script.py


<p align="center">
      <img src="https://github.com/caresiop/GSC-AVL-Script/blob/main/images/UI.png?raw=true" width="387" height="566" />
</p>

### Buttons:
- **Record**: Starts ``Audacity`` recording
- **Pause**: Pauses ``Audacity`` recording
- **Clear**: Clears ``Audacity`` recording
- **Save**: Saves ``Audacity`` recording onto local save directory
- **Local Files**: Opens local save directory
- **Upload**: Uploads ``.mp3`` file(s) from local save directory onto respective ``Google Drive`` folder(s) and then displays respective link(s) onto app text editor
- **Copy**: Copies current text on app text editor onto clipboard

### Features:
- Drop down menu can be manually edited to include other file titles
  - Unfamiliar file titles will be placed in ``Google Drive`` 'Misc' folder
- If program is closed and files aren't uploaded to ``Google Drive``, they can be uploaded on next program start up
- ``Cross Seeds`` check box for church youth group service
  - Locks session into ``Cross Seeds`` session once file is saved locally to ensure ``GSC`` files and ``Cross Seeds`` files are not uploaded into incorrect ``Google Drive`` folder(s)
- If user empties local save directory manually, app will recognize there are no files to upload and unlock session

### Workflow:

      Record/Pause/Clear -> Save -> Upload -> Copy
