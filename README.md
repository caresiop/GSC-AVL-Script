# GSC-AVL-Script

Installation
------------
Application: Audacity
Link: https://www.audacityteam.org/ (version 3)

Packages: PyQT5, send2trash, Google API

PyQT5
Link: https://pypi.org/project/PyQt5/
.. code-block:: sh
  pip3 install PyQT5

send2Trash
Link: https://pypi.org/project/Send2Trash/
.. code-block:: sh
  pip3 install send2trash

Google API
Link: https://developers.google.com/docs/api/quickstart/python

.. code-block:: sh

  pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Set Up
------
Audacity:
- Enable 'mod-script-pipe'
.. code-block:: sh
  
  Preferences -> Modules -> Enable 'mod-script-pipe'

Google Cloud
Tutorial: https://www.youtube.com/watch?v=6bzzpda63H0
- Download client file, rename it, add it to directory

config.py:
- Fill config.py file with local paths and Google folder ids

.. code-block:: sh

    config = {
        'audacity': {
            'app_path': '' # local path to 'Audacity' app
        },
        'local': {
            'save_path': '' # local path to 'local_recordings' folder
        },
        'google': {
            'credentials_path': '', # local path to 'credentials.json'
            'parent': '' # Google Drive Parent folder
        },
        # Google Drive folder IDs (https://drive.google.com/drive/folders/[id found here])
        'good_stewards_service': {
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

Usage
-----
