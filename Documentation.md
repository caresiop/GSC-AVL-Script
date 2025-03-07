### ``GSC_Recording_Script.py``

# ``Class MainWindow``

## Table of Contents

[Start up](#start-up)
- [``start_up()``](#start_up)
- [``open_message_box()``](#open_message_box)

[Exit](#exit)
- [``closeEvent()``](#closeEvent)

[UI Functions](#UI-functions)
- [``record()``](#record)
- [``pause()``](#pause)
- [``clear()``](#clear)
- [``save()``](#save)
- [``upload()``](#upload)
- [``open_directory()``](#open_directory)
- [``copy()``](#copy)
- [``check_box_update()``](#check_box_update)

[Helper Functions](#helper-functions)
- [``disable_buttons()``](#disable_buttons)
- [``update_record_state()``](#update_record_state)
- [``update_upload_state()``](#update_upload_state)
- [``enable_local_files_copy()``](#enable_local_files)
- [``list_files_box()``](#list_files_box)
- [``get_links()``](#get_links)
- [``clean_directory()``](#clean_directory)
- [``empty_directory()``](#empty_directory)
- [``check_directory()``](#check_directory)

[Message Box Functions](#message-box-functions)
- [``create_message_box()``](#create_message_box)
- [``create_warning_box()``](#create_warning_box)
- [``user_prompt_box()``](#user_prompt_box)
- [``curr_record_prompt()``](#curr_record_prompt)

---

## Start up

### ``start_up()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Checks whether there are files in local save directory from a previous session; if so, restores session

**UI states**:
- **Enabled**: ``None``
- **Disabled**: ``None``
- **Conditional**: ``Cross Seeds``, ``Upload``

**Pseudocode**:

- Call ``clean_directory()`` (often ``.DS_Store`` makes its way into the local save directory)
- Check whether there are files in local save directory (``check_directory()``)
  - **True**:
    - Obtain ``list`` of files in local save directory
    - Check whether the files in local save directory are from a 'GSC' session or 'Cross Seeds' session
      - **'GSC'**:
        - Notify user of 'GSC' session
        - Message box user of continued 'GSC' session 
      - **'Cross Seeds'**:
        - Set ``cross_seeds_flag`` to ``True``
        - Call ``cross_seeds_check_box()`` with parameter ``True`` to notify function of start up
    - Enable ``Upload`` button (there are files to upload)
    - Disable ``Cross Seeds`` check box (lock session)
  - **False**:
    - Notify user of default `GSC` session 
    - Call ``open_message_box()`` to message box user of ``Audacity`` app requirements
- Call ``open_message_box`` to message box user ``Audacity`` app configurations

---

### ``open_message_box()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Start up message box notifying user of necessary ``Audacity`` app configurations

---

## Exit

### ``closeEvent()`` 

**Note**: Overloaded ``PyQT5`` close function

- **Parameters**: ``QCloseEvent event``

- **Return**: ``None``

**Description**: Checks whether there are files in local save directory from a previous session; if so, restores session

**Pseudocode**:

- Call ``clean_directory()`` (often ``.DS_Store`` makes its way into the local save directory)
- Call ``check_directory()`` to update ``file_flag``
- Check whether there is a recording in progress (``curr_recording_flag``)
  - **True**:
    - Prompt user of recording in progress and whether they would still like to exit
      - **Yes** 
        - Check whether there are files in local save directory
            - **True**:
              - Prompt user of files to be uploaded and whether they would still like to exit
                - **Yes**:
                  - Call ``Audacity`` function ``exit()``
                  - ``event.accept()`` (closes program)
                - **No**:
                  - ``event.ignore()``
            - **False**
              - Call ``Audacity`` function ``exit()``
                - ``event.accept()`` (closes program)
      - **No**
        - ``event.ignore()`` 
  - **False** (``elif``) Check whether there are files in local save directory
      - **True**:
        - Prompt user of files to be uploaded and whether they would still like to exit
          - **Yes**:
            - Call ``Audacity`` function ``exit()``
            - ``event.accept()`` (closes program)
          - **No**:
            - ``event.ignore()``
  - **False**
    - ``event.ignore()`` 

---

## UI Functions

### ``record()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Calls ``Audacity`` command ``record_audio()``

**UI states**:
- **Enabled**: ``Pause``, ``Local Files``, ``Copy``
- **Disabled**: ``Record``
- **Conditional**: ``Clear/Save`` (``curr_recording_flag``->``update_record_state()``), ``Upload`` (``file_flag``->``update_upload_state()``)

**Pseudocode**:

1. **User notification**
  - Notify user that ``record()`` has been called
2. **UI changes**
  - If ``Pause`` button color is Yellow, set the ``Pause`` button color to Grey
  - Set ``Record`` button color to Green
  - Disable all buttons (``disable_buttons()``) so no new functions can be queued
3. **Execute**
  - Call Audacity record command (``record_audio()``)
  - Set ``curr_recording_flag`` to ``True`` (there is currently a recording in progress)
  - Set ``record_state_flag`` to ``True`` (currently in ``record`` state)
4. **Restore UI states**
  - Disable ``Record`` button
  - Enable ``Pause`` button
  - Enable ``Upload`` button if files saved to upload (``file_flag``->``update_record_state()``)
  - Enable ``Local Files`` and ``Copy`` buttons (``enable_local_files_copy()``)

---

### ``pause()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Calls ``Audacity`` command ``pause_audio()``

**UI states**:
- **Enabled**: ``Record``, ``Local Files``, ``Copy``
- **Disabled**: ``Pause``
- **Conditional**: ``Clear/Save`` (``curr_recording_flag``-> ``update_record_state()``), ``Upload`` (``file_flag``-> ``update_upload_state()``)

**Pseudocode**:

1. **User notification**
  - Notify user that ``pause()`` has been called
2. **UI changes**
  - If ``Record`` button color is Green, set the ``Record`` button color to Grey
  - Set ``Pause`` button color to Yellow
  - Disable all buttons (``disable_buttons()``) so no new functions can be queued
3. **Execute**
  - Call Audacity record command (``stop_audio()``)
  - Set ``record_state_flag`` to ``False`` (currently in ``pause`` state)
4. **Restore UI states**
  - Disable ``Pause`` button
  - Enable ``Record`` button
  - Enable ``Upload`` button if files saved to upload (``file_flag``->``update_record_state()``)
  - Enable ``Local Files`` and ``Copy`` buttons (``enable_local_files_copy()``)

---
  
### ``clear()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Calls ``Audacity`` command ``clear_audio()``

**UI states**:
  - **Prompt**:
    - **Yes**:
      - **Enabled**: ``Record``, ``Local Files``, ``Copy``
      - **Disabled**: ``Pause``,  ``Clear``, ``Save``
      - **Conditional**: ``Upload`` (``file_flag``->``update_upload_state()``)
    - **No**:
      - **Enabled**: ``Clear``, ``Save``, ``Local Files``, ``Copy``
      - **Disabled**: ``None``
      - **Conditional**: ``Record/Pause, Clear/Save`` (``curr_recording_flag``, ``record_state_flag``->``update_record_state()``)
  
**Pseudocode**:

1. **User notification**
  - Notify user that ``clear()`` has been called
2. **UI changes**
  - Set ``Record/Pause`` button colors to Grey
  - Set ``Clear`` button to Red
  - Disable all buttons (``disable_buttons()``) so no new functions can be queued
3. **Execute**
  - Prompt user whether they are sure they want to clear the recording
    - **Yes**:
      - Call Audacity record command (``clear_audio()``)
      - Set ``curr_recording_flag`` to ``False`` (there is currently no recording in progress)
      - Enable ``Record`` button
      - Notify user that recording has been cleared
4. **Restore UI states**
  - If ``curr_recording_flag``, enable ``Clear/Save`` buttons (recording was not cleared)
     - If ``record_state_flag``, restore ``Record/Pause`` buttons and their respective colors
  - Enable ``Upload`` button if files saved to upload (``file_flag``->(``update_record_state()``))
  - Enable ``Local Files`` and ``Copy`` buttons (``enable_local_files_copy()``)
  - Set ``Clear`` button to Grey

---

### ``save()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Calls ``Audacity`` command ``save_audio()``

**UI states**:
  - **Prompt**:
    - **Yes**:
      - **Enabled**: ``Record``, ``Local Files``, ``Copy``
      - **Disabled**: ``Pause``,  ``Clear``, ``Save``
      - **Conditional**: ``Upload`` (``file_flag``->``update_upload_state()``)
    - **No**:
      - **Enabled**: ``Clear``, ``Save``, ``Local Files``, ``Copy``
      - **Disabled**: ``None``
      - **Conditional**: ``Record/Pause, Clear/Save`` (``curr_recording_flag``, ``record_state_flag``->``update_record_state()``)
  
**Pseudocode**:

1. **User notification**
  - Notify user that ``save()`` has been called
2. **UI changes**
  - Set ``Record/Pause`` button colors to Grey
  - Set ``Save`` button to Blue
  - Disable all buttons (``disable_buttons()``) so no new functions can be queued
    - *Note*: If first save of session is successful, user will be locked into their respective session ('GSC' or 'Cross Seeds') to ensure that session files are not mixed
3. **Execute**
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
4. **Restore UI states**
  - If ``curr_recording_flag``, enable ``Clear/Save`` buttons (recording was not saved)
     - If ``record_state_flag``, restore ``Record/Pause`` buttons and their respective colors
  - Enable ``Upload`` button if files saved to upload (``file_flag``->(``update_record_state()``))
  - Enable ``Local Files`` and ``Copy`` buttons (``enable_local_files_copy()``)
  - Set ``Save`` button to Grey

---

### ``upload()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Calls ``GoogleCloud`` command ``exec()`` and prints session ``music_links``, ``sermon_links``, ``misc_links`` onto UI text box

**UI states**:
  - **Prompt**:
    - **Yes**:
      - **Enabled**: ``Record``, ``Local Files``, ``Copy``
      - **Disabled**: ``Pause``,  ``Clear``, ``Save``
      - **Conditional**: ``Upload`` (``file_flag``->``update_upload_state()``)
    - **No**:
      - **Enabled**: ``Clear``, ``Save``, ``Local Files``, ``Copy``
      - **Disabled**: ``None``
      - **Conditional**: ``Record/Pause, Clear/Save`` (``curr_recording_flag``, ``record_state_flag``->``update_record_state()``)
  
**Pseudocode**:

1. **User notification**
  - Notify user that ``upload()`` has been called
2. **UI changes**
  - Set ``Record/Pause`` button colors to Grey
  - Set ``Upload`` button to Blue
  - Disable all buttons (``disable_buttons()``) so no new functions can be queued
3. **Execute**
  - Clean local save directory to only hold ``.mp3`` files (``clean_directory()``)
  - Check if there are files in the local save directory (``check_directory()``)
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
4. **Restore UI states**
  - Enable ``Record`` button (regardless of prompt answers, ``Record`` needs to be enabled; if there is a recording in progress, the correct button will be set to its respective state via ``curr_recording_flag``)
  - If ``curr_recording_flag``, enable ``Clear/Save`` buttons (recording was not saved)
     - If ``record_state_flag``, restore ``Record/Pause`` buttons and their respective colors
  - Enable ``Upload`` button if files saved to upload (``file_flag``->(``update_record_state()``))
  - Enable ``Local Files`` and ``Copy`` buttons (``enable_local_files_copy()``)
  - Set ``Upload`` button to Grey

---

### ``open_directory()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Calls ``subprocess`` command to open local save directory window

**Pseudocode**:

1. **UI changes**
  - Set ``Local Files`` button color to Blue
2. **Execute**
  - Check whether the path exists (``os.path.exists(*path*)``)
    - **Yes**:
      - Open local save directory window (``subprocess.run(['open', *path*]``) 
    - **No**:
      - Warning box user that the local save path is invalid and to reconfigure
3. **UI changes**
  - Set ``Local Files`` button color to Grey

---

### ``copy()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Copies text in UI text box into clipboard

**Pseudocode**:

1. UI changes
  - Set ``Copy`` button color to Blue
2. Execute
  - Call QTextEdit function ``selectAll()``
  - Call QTextEdit function ``copy()``
3. UI changes
  - Set ``Copy`` button color to Grey

---

### ``check_box_update()`` 

- **Parameters**: ``bool start_up = None``

- **Return**: ``None``

**Description**: Check mark box function; message box and notifies user when state/session is changed

**Pseudocode**:

- Check whether the ``cross_seeds_check_box`` is checked
  - **True**:
    - Set ``cross_seeds_flag`` to ``False``
    - Call ``GoogleCloud`` function ``cross_seeds`` to notify ``GoogleCloud`` instance that the session is in `GSC`
    - Notify user that a `GSC` session is starting
    - Message box user of new `GSC` session
  - **False**:
    - Set ``cross_seeds_flag`` to ``True``
    - Call ``GoogleCloud`` function ``cross_seeds`` to notify ``GoogleCloud`` instance that the session is in `Cross Seeds`
    - Notify user that the session of new session
      - if ``start_up`` parameter is ``True``
        -  **True**:
          - Message box user of continuing previous `Cross Seeds` session
        -  **False**:
          - Message box user of new `Cross Seeds` session
  
**Developer Notes**

For whatever reason, the logic is flipped. As to why, I am not sure.

One would think ``state == cross_seeds_check_box.isChecked()`` would return ``True`` if the check box is checked.
  
---

## Helper Functions

### ``disable_buttons()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Disables all buttons

**UI states**:
  - **Enabled**: ``None``
  - **Disabled**: ``Cross Seeds``, ``Record``, ``Pause``, ``Clear``, ``Save``, ``Upload``, ``Local Files``, ``Copy``
  - **Conditional**: ``None``

**Pseudocode**:

- Disable ``Cross Seeds`` check box and ``Record``, ``Pause``, ``Clear``, ``Save``, ``Upload``, ``Local Files``, ``Copy`` buttons
  
---

### ``update_record_state()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Checks whether there is a recording in progress and which state the recording is in (``Record/Pause``)

**UI states**:
  - **Enabled**: ``None``
  - **Disabled**: ``None``
  - **Conditional**: ``Record/Pause, Clear/Save`` (``curr_recording_flag``, ``record_state_flag``)

**Pseudocode**:

- Check ``curr_recording_flag`` to see if there is currently a recording in session
  - **True**:
    - Enable ``Clear/Save`` buttons
    - Check ``record_state_flag`` to see whether ``Record`` is active or ``Pause`` is active
      - **True**:
        - Set ``Record`` button to Green
        - Set ``Pause`` button to Grey
        - Enable ``Record`` button
        - Disable ``Pause`` button
      - **False**:
        - Set ``Pause`` button to Yellow
        - Set ``Record`` button to Grey
        - Enable ``Pause`` button
        - Disable ``Record`` button

---

### ``update_upload_state()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Checks whether there are files in the local directory, and if so, enables ``Upload`` button

**UI states**:
  - **Enabled**: ``None``
  - **Disabled**: ``None``
  - **Conditional**: ``Upload`` (``file_flag``)

**Pseudocode**:

- Check ``file_flag`` to see if there are files in the local directory
  - **True**:
    - Enable ``Upload`` button
      
--- 

### ``enable_local_files_copy()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Enables ``Local Files/Copy`` buttons

**UI states**:
  - **Enabled**: ``Local Files``, ``Copy``
  - **Disabled**: ``None``
  - **Conditional**: ``None``

**Pseudocode**:

- Enable ``Local Files`` button
- Enable ``Copy`` button
  
---

### ``list_files_box()`` 

- **Parameters**: ``None``

- **Return**: ``string text``

**Description**: Checks local directory and returns all files names in a formatted printable ``string``

**Pseudocode**:

- Grab file names as ``list`` from local save directory (``os.listdir(*path*)``)
- Sort ``list`` into alphabetical/numerical order
- Create an empty ``string`` variable
- Iterate through ``list`` and append file name to ``string`` variable on each iteration
- Return ``string`` variable
  
---

### ``get_links()`` 

- **Parameters**: ```list links``` 

- **Return**: ``None``

**Description**: Iterates through passed ``list`` and prints out each indexed files's ``name`` and ``link`` into the UI text box; if there are duplicates of the same title, append a letter of the alphabetic to the end of the title, starting with 'a'; increment and append alphabetic character as long as ``name`` is the same

**Pseudocode**:

Execute
  - Check whether there is more than 1 file in ``list``
    - **True**:
      - Create a varibale ``count`` and initialize it to ``int`` value ``0``
      - Check whether the index value is the start of ``list``, the end of ``list``, or in the middle of ``list``
        - **Start**:
          - Check whether the title of this file matches the file of the next index
            - **True**:
              - Print to UI text box, appending alphabetic character of index ``count``
              - Increment ``count``
            - **False**:
              - Print to UI text box normally
        - **End**:
          - Check whether the title of this file matches the file previously
            - **True**:
              - Print to UI text box, appending alphabetic character of index ``count``
            - **False**:
              - Print to UI text box normally
        - **Middle**:
          - Check whether the title of this file does not match the file previously (indicates a new file)
            - **True**:
              - Set ``count`` to ``0``
          - Check whether the title of this file matches the previous file or whether the title of this file matches the next file
            - **True**: 
              - Print to UI text box, appending alphabetic character of index ``count``
              - Increment ``count``
            - **False**:
              - Print to UI text box normally  
    - **False**:
      - Print single file to UI text box normally
      
**Developer Notes**: Who would have thought there would be an algorithms problem in this simple app? A dictionary would make the solution simple, but I wanted to try and keep constant space.
- Time Complexity: ``O(n)``, Space Complexity: ``O(1)``

---

### ``clean_directory()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Checks local save directory and sends to trash all non ``.mp3`` files

**Pseudocode**:

- Iterate through all files and directories in local save directory (``os.walk(*path*)``)
  - Iterate through files and send to trash any files not containing ``.mp3``
  - Iterate through directories and send to trash all directories
    
---

### ``empty_directory()`` 

- **Parameters**: ``None``

- **Return**: ``None``

**Description**: Sends to trash all files and all direectories in local save directory

**Pseudocode**:

- Iterate through all files and directories in local save directory (``os.walk(*path*)``)
  - Iterate through files and send to trash all files
  - Iterate through directories and send to trash all directories
    
---

### ``check_directory()`` 

- **Parameters**: ``None``

- **Return**: ``bool``

**Description**: Checks whether there are any files in the directory

**Pseudocode**:

- Grab list of files from local save directory (``os.listdir(*path*)``)
- Check whether there are files in the list
  - **True**:
    - Set ``file_flag`` to ``True``
    - Return ``True``
  - **False**:
    - Set ``file_flag`` to ``False``
    - Return ``False`` 

---

## Message Box Functions

### ``create_message_box()`` 

- **Parameters**: ``string message``

- **Return**: ``None``

**Description**: Message box that displays passed ``string``

---

### ``create_warning_box()`` 

- **Parameters**: ``string message``

- **Return**: ``None``

**Description**: Warning box that displays passed ``string``

---

### ``user_prompt_box()`` 

- **Parameters**: ``string text``, ``string informative_text``

- **Return**: ``bool``

**Description**: User prompt that takes passed ``text`` for window title and passed ``informative_text`` for window info; returns ``True`` if user answers ``Yes`` and returns ``False`` if user answers ``No``

---

### ``curr_record_prompt_box()`` 

- **Parameters**: ``None``

- **Return**: ``bool``

**Description**: Message box that prompts user if there is a recording in progress

**Pseudocode**:

- Check ``curr_recording_flag``
  - **True**:
    - return (Prompt user whether they wish to continue)
  - **False**:
    - return ``True`` 
