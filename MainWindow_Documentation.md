# GSC_Recording_Script.command

## Class MainWindow

### Button Functions

### ``record()`` 

- **Parameters**: None

- **Return**: None

**Description**: Calls ``Audacity`` command ``record_audio()``

**On-click UI button states**:
  - **Enabled**: ``Pause``, ``Local Files``, ``Copy``
  - **Disabled**: ``Record``
  - **Conditional**: ``Clear/Save`` (``curr_recording_flag``->``update_record_state()``), ``Upload`` (``file_flag``->``update_upload_state()``)

**Pseudocode**:

1. User notification
    - Notify user that ``record()`` has been called
2. UI changes
    - If ``Pause`` button color is Yellow, set the ``Pause`` button color to Grey
    - Set ``Record`` button color to Green
    - Disable all buttons (``disable_all_buttons()``) so no new functions can be queued
3. Execute
    - Call Audacity record command (``record_audio()``)
    - Set ``curr_recording_flag`` to ``True`` (there is currently a recording in progress)
    - Set ``record_state_flag`` to ``True`` (currently in ``record`` state)
4. Restore button states
    - Disable ``Record`` button
    - Enable ``Pause`` button
    - Enable ``Upload`` button if files saved to upload (``file_flag``->``update_record_state()``)
    - Enable ``Local Files`` and ``Copy`` buttons (``enable_local_files_copy()``)

---

### ``pause()`` 

- **Parameters**: None

- **Return**: None

**Description**: Calls ``Audacity`` command ``pause_audio()``

**On-click UI button states**:
  - **Enabled**: ``Record``, ``Local Files``, ``Copy``
  - **Disabled**: ``Pause``
  - **Conditional**: ``Clear/Save`` (``curr_recording_flag``-> ``update_record_state()``), ``Upload`` (``file_flag``-> ``update_upload_state()``)

**Pseudocode**:

1. User notification
    - Notify user that ``pause()`` has been called
2. UI changes
    - If ``Record`` button color is Green, set the ``Record`` button color to Grey
    - Set ``Pause`` button color to Yellow
    - Disable all buttons (``disable_all_buttons()``) so no new functions can be queued
3. Execute
    - Call Audacity record command (``stop_audio()``)
    - Set ``record_state_flag`` to ``False`` (currently in ``pause`` state)
4. Restore button states
    - Disable ``Pause`` button
    - Enable ``Record`` button
    - Enable ``Upload`` button if files saved to upload (``file_flag``->``update_record_state()``)
    - Enable ``Local Files`` and ``Copy`` buttons (``enable_local_files_copy()``)

---
  
### ``clear()`` 

- **Parameters**: None

- **Return**: None

**Description**: Calls ``Audacity`` command ``clear_audio()``

**On-click UI button states**:
  - **Prompt**:
    - **Yes**:
      - **Enabled**: ``Record``, ``Local Files``, ``Copy``
      - **Disabled**: ``Pause``,  ``Clear``, ``Save``
      - **Conditional**: ``Upload`` (``file_flag``->``update_upload_state()``)
    - **No**:
      - **Enabled**: ``Clear``, ``Save``, ``Local Files``, ``Copy``
      - **Disabled**: None
      - **Conditional**: ``Record/Pause, Clear/Save`` (``curr_recording_flag``, ``record_state_flag``->``update_record_state()``)
  
**Pseudocode**:

1. User notification
    - Notify user that ``clear()`` has been called
2. UI changes
    - Set ``Record/Pause`` button colors to Grey
    - Set ``Clear`` button to Red
    - Disable all buttons (``disable_all_buttons()``) so no new functions can be queued
3. Execute
    - Prompt user whether they are sure they want to clear the recording
      - **Yes**:
        - Call Audacity record command (``clear_audio()``)
        - Set ``curr_recording_flag`` to ``False`` (there is currently no recording in progress)
        - Enable ``Record`` button
        - Notify user that recording has been cleared
      - **No**:
        - None
4. Restore button states
    - If ``curr_recording_flag``, enable ``Clear/Save`` buttons (recording was not cleared)
       - If ``record_state_flag``, restore ``Record/Pause`` buttons and their respective colors
    - Enable ``Upload`` button if files saved to upload (``file_flag``->(``update_record_state()``))
    - Enable ``Local Files`` and ``Copy`` buttons (``enable_local_files_copy()``)
    - Set ``Clear`` button to Grey

---

### ``save()`` 

- **Parameters**: None

- **Return**: None

**Description**: Calls ``Audacity`` command ``save_audio()``

**On-click UI button states**:
  - Prompt:
    - **Yes**:
      - **Enabled**: ``Record``, ``Local Files``, ``Copy``
      - **Disabled**: ``Pause``,  ``Clear``, ``Save``
      - **Conditional**: ``Upload`` (``file_flag``->``update_upload_state()``)
    - **No**:
      - **Enabled**: ``Clear``, ``Save``, ``Local Files``, ``Copy``
      - **Disabled**: None
      - **Conditional**: ``Record/Pause, Clear/Save`` (``curr_recording_flag``, ``record_state_flag``->``update_record_state()``)
  
**Pseudocode**:

1. User notification
    - Notify user that ``save()`` has been called
2. UI changes
    - Set ``Record/Pause`` button colors to Grey
    - Set ``Save`` button to Blue
    - Disable all buttons (``disable_all_buttons()``) so no new functions can be queued
      - Note: If first save of session is successful, user will be locked into their respective session ('GSC' or 'Cross Seeds') to ensure that session files are not mixed
3. Execute
    - Prompt user whether they are sure they want to save the recording
      - **Yes**:
        - Grab text from the drop-down menu (``combo_box``)
        - Call Audacity record command (``save_audio()``) with the argument of the drop-down menu title/index
          - **Successful**:
            - Message box user of successful local save
            - Determine if GSC or Cross Seeds session
              - Rename file using date, time, session, and drop-down menu title
            - Set ``curr_recording_flag`` to ``False`` (there is currently no recording in progress)
            - Set ``file_flag`` to ``True`` (there is now a file in the local folder)
            - Enable ``Record`` button
            - Notify user that recording has been saved
          - **Failure**:
            - Warning box user of failed local save
            - Notify user that recording was not saved
      - **No**:
        - Enable ``Save`` button
        - If there is no file that was saved (``file_flag``), unlock session by enabling ``cross_seeds_check_button``
4. Restore button states
    - If ``curr_recording_flag``, enable ``Clear/Save`` buttons (recording was not saved)
       - If ``record_state_flag``, restore ``Record/Pause`` buttons and their respective colors
    - Enable ``Upload`` button if files saved to upload (``file_flag``->(``update_record_state()``))
    - Enable ``Local Files`` and ``Copy`` buttons (``enable_local_files_copy()``)
    - Set ``Save`` button to Grey

---

### ``upload()`` 

- **Parameters**: None

- **Return**: None

**Description**: Calls ``GoogleCloud`` command ``exec()`` and prints session ``music_links``, ``sermon_links``, ``misc_links`` onto UI text box

**On-click UI button states**:
  - Prompt:
    - **Yes**:
      - **Enabled**: ``Record``, ``Local Files``, ``Copy``
      - **Disabled**: ``Pause``,  ``Clear``, ``Save``
      - **Conditional**: ``Upload`` (``file_flag``->``update_upload_state()``)
    - **No**:
      - **Enabled**: ``Clear``, ``Save``, ``Local Files``, ``Copy``
      - **Disabled**: None
      - **Conditional**: ``Record/Pause, Clear/Save`` (``curr_recording_flag``, ``record_state_flag``->``update_record_state()``)
  
**Pseudocode**:

1. User notification
    - Notify user that ``upload()`` has been called
2. UI changes
    - Set ``Record/Pause`` button colors to Grey
    - Set ``Upload`` button to Blue
    - Disable all buttons (``disable_all_buttons()``) so no new functions can be queued
3. Execute
    - Clean local_folder to only hold ``.mp3`` files (``clean_directory()``)
    - Check if there are files in the directory
        - Empty:
          - Warning box user that there are no files to upload, and that the current session will be unlocked
            - Enable ``Record`` button
            - Unlock session by enabling ``cross_seeds_check_button``
        - Files present:
          - Check if there is a recording in progress (``curr_recording_flag``->``curr_record_prompt``); if so, prompt user whether they are sure they want to save the recording
            - **Yes**:
              - Prompt user whether they want to upload to Google Drive; if so, list files to be uploaded and prompt user whether they want to upload the following files
                - **Yes**:
                  - Call ``GoogleCloud`` execute command (``exec()``)
                  - Clear UI text box (``text_edit``)
                  - Write date and respective session to UI text box
                  - Print links to UI text box using ``get_links()`` function with ``GoogleCloud`` functions ``get_music_links``, ``get_sermon_links``, ``get_misc_links``
                  - Empty local directory (``empty_directory``)
                  - Message box user that upload was successful
                  - Set ``file_flag`` to ``False`` because there are no files in local directory
                  - Unlock session by enabling ``cross_seeds_check_button``
                - **No**:
                  - None 
            - **No**:
              - None
4. Restore button states
    - Enable ``Record`` button (regardless of prompt answers, ``Record`` needs to be enabled; if there is a recording in progress, the correct button will be set to its respective state via ``curr_recording_flag``)
    - If ``curr_recording_flag``, enable ``Clear/Save`` buttons (recording was not saved)
       - If ``record_state_flag``, restore ``Record/Pause`` buttons and their respective colors
    - Enable ``Upload`` button if files saved to upload (``file_flag``->(``update_record_state()``))
    - Enable ``Local Files`` and ``Copy`` buttons (``enable_local_files_copy()``)
    - Set ``Upload`` button to Grey

---

### ``open_directory()`` 

- **Parameters**: None

- **Return**: None

**Description**: Calls ``subprocess`` command to open local save directory window

**On-click UI button states**:
  - None

**Pseudocode**:

1. UI changes
    - Set ``Local Files`` button color to Blue
3. Execute
    - Check whether the path exists (``os.path.exists(*path*)``)
      - **Yes**:
        - Open local save directory window (``subprocess.run(['open', *path*]``) 
      - **No**:
        - Warning box user that the local save path is invalid and to reconfigure
4. UI changes
    - Set ``Local Files`` button color to Grey

---

### ``copy()`` 

- **Parameters**: None

- **Return**: None

**Description**: Copies text in UI text box into clipboard

**On-click UI button states**:
  - None

**Pseudocode**:

1. UI changes
    - Set ``Copy`` button color to Blue
3. Execute
    - Call QTextEdit function ``selectAll()``
    - Call QTextEdit function ``copy()``
4. UI changes
    - Set ``Copy`` button color to Grey
  
---
