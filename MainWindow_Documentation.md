### ``GSC_Recording_Script.command``

# ``Class MainWindow``

[Button Functions](#button-functions)
- [record](#record)

[Helper Functions](#helper-functions)

---

## Button Functions

### ``record()`` 

- **Parameters**: None

- **Return**: None

**Description**: Calls ``Audacity`` command ``record_audio()``

**UI button states**:
  - **Enabled**: ``Pause``, ``Local Files``, ``Copy``
  - **Disabled**: ``Record``
  - **Conditional**: ``Clear/Save`` (``curr_recording_flag``->``update_record_state()``), ``Upload`` (``file_flag``->``update_upload_state()``)

**Pseudocode**:

1. User notification
    - Notify user that ``record()`` has been called
2. UI changes
    - If ``Pause`` button color is Yellow, set the ``Pause`` button color to Grey
    - Set ``Record`` button color to Green
    - Disable all buttons (``disable_buttons()``) so no new functions can be queued
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

**UI button states**:
  - **Enabled**: ``Record``, ``Local Files``, ``Copy``
  - **Disabled**: ``Pause``
  - **Conditional**: ``Clear/Save`` (``curr_recording_flag``-> ``update_record_state()``), ``Upload`` (``file_flag``-> ``update_upload_state()``)

**Pseudocode**:

1. User notification
    - Notify user that ``pause()`` has been called
2. UI changes
    - If ``Record`` button color is Green, set the ``Record`` button color to Grey
    - Set ``Pause`` button color to Yellow
    - Disable all buttons (``disable_buttons()``) so no new functions can be queued
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

**UI button states**:
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
    - Disable all buttons (``disable_buttons()``) so no new functions can be queued
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

**UI button states**:
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
    - Disable all buttons (``disable_buttons()``) so no new functions can be queued
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

**UI button states**:
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
    - Disable all buttons (``disable_buttons()``) so no new functions can be queued
3. Execute
    - Clean local_folder to only hold ``.mp3`` files (``clean_directory()``)
    - Check if there are files in the directory (``check_directory()``)
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

**UI button states**:
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

## Helper Functions

### ``check_box_update()`` 

- **Parameters**: ``bool start_up = None``

- **Return**: None

**Description**: Check mark box function; message box and notifies user when state/session is changed

**On-click UI button states**:
  - None

**Pseudocode**:

1. Execute
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

### ``disable_buttons()`` 

- **Parameters**: None

- **Return**: None

**Description**: Disables all buttons

**UI button states**:
  - **Enabled**: None
  - **Disabled**: ``Cross Seeds``, ``Record``, ``Pause``, ``Clear``, ``Save``, ``Upload``, ``Local Files``, ``Copy``
  - **Conditional**: None

**Pseudocode**:

1. Execute
   - Disable ``Cross Seeds`` check box and ``Record``, ``Pause``, ``Clear``, ``Save``, ``Upload``, ``Local Files``, ``Copy`` buttons
  
---

### ``update_record_state()`` 

- **Parameters**: None

- **Return**: None

**Description**: Checks whether there is a recording in progress and which state the recording is in (``Record/Pause``)

**UI button states**:
  - **Enabled**: None
  - **Disabled**: None
  - **Conditional**: ``Record/Pause, Clear/Save`` (``curr_recording_flag``, ``record_state_flag``)

**Pseudocode**:

1. Execute
   - Check ``curr_recordig_flag`` to see if there is currently a recording in session
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
     - **False**:
       - None

---

### ``update_upload_state()`` 

- **Parameters**: None

- **Return**: None

**Description**: Checks whether there are files in the local directory, and if so, enables ``Upload`` button

**UI button states**:
  - **Enabled**: None
  - **Disabled**: None
  - **Conditional**: ``Upload`` (``file_flag``)

**Pseudocode**:

1. Execute
   - Check ``file_flag`` to see if there are files in the local directory
     - **True**:
       - Enable ``Upload`` button
     - **False**:
       - None
      
--- 

### ``enable_local_files_copy()`` 

- **Parameters**: None

- **Return**: None

**Description**: Enables ``Local Files/Copy`` buttons

**UI button states**:
  - **Enabled**: ``Local Files``, ``Copy``
  - **Disabled**: None
  - **Conditional**: None

**Pseudocode**:

1. Execute
   - Enable ``Local Files`` button
   - Enable ``Copy`` button
  
---

### ``list_files_box()`` 

- **Parameters**: None

- **Return**: ``string text``

**Description**: Checks local directory and returns all files names in a formatted printable string

**Pseudocode**:

1. Execute
   - Grab file names as list from local save directory (``os.listdir(*path*)``)
   - Sort the list into alphabetical/numerical order
   - Create an empty string variable
   - Iterate through the list and append file name to string variable on each iteration
   - Return string variable
  
---

### ``get_links()`` 

- **Parameters**: ```list links``` 

- **Return**: None

**Description**: Iterates through passed list and prints out each indexed files's name and link into the UI text box; if there are duplicates of the same title, it will append a letter of the alphabet, starting with 'a', and will increment as long as the name is the same

**Pseudocode**:

1. Execute
   - Check whether there is more than 1 file in the list
     - **True**:
       - Create a varibale ``count`` and initialize it to int value ``0``
       - Check whether the index value is the start of the list, the end of the list, or in the middle
         - **Start**:
           - Check whether the title of this file matches the file of the next index
             - **True**:
               - Print to UI text box, appending alphabet character of index ``count``
               - Increment ``count``
             - **False**:
               - Print to UI text box normally
         - **End**:
           - Check whether the title of this file matches the file previously
             - **True**:
               - Print to UI text box, appending alphabet character of index ``count``
             - **False**:
               - Print to UI text box normally
         - **Middle**:
           - Check whether the title of this file does not match the file previously (indicates a new file)
             - **True**:
               - Set ``count`` to ``0``
             - **False**:
               - None
           - Check whether the title of this file matches the previous file or whether the title of this file matches the next file
             - **True**: 
               - Print to UI text box, appending alphabet character of index ``count``
               - Increment ``count``
             - **False**:
               - Print to UI text box normally  
     - **False**:
       - Print single file to UI text box normally
      
**Developer Notes**: Who would have thought there would be an algorithms problem in this simple app? I believe this problem could have been brute forced, but I wanted to make an efficient solution.
- Time Complexity: ``O(n)``, Space Complexity: ``O(1)``

---

### ``clean_directory()`` 

- **Parameters**: None

- **Return**: None

**Description**: Checks local save directory and sends to trash all non ``.mp3`` files

**Pseudocode**:

1. Execute
   - Iterate through all files and directories in local save directory (``os.walk(*path*)``)
     - Iterate through files and send to trash any files not containing ``.mp3``
     - Iterate through directories and send to trash all directories
    
---

### ``empty_directory()`` 

- **Parameters**: None

- **Return**: None

**Description**: Sends to trash all files and all direectories in local save directory

**Pseudocode**:

1. Execute
   - Iterate through all files and directories in local save directory (``os.walk(*path*)``)
     - Iterate through files and send to trash all files
     - Iterate through directories and send to trash all directories
    
---

### ``check_directory()`` 

- **Parameters**: None

- **Return**: ``bool``

**Description**: Checks whether there are any files in the directory

**Pseudocode**:

1. Execute
   - Grab list of files from local save directory (``os.listdir(*path*)``)
   - Check whether there are files in the list
     - **True**:
       - Set ``file_flag`` to ``True``
       - Return ``True``
     - **False**:
       - Set ``file_flag`` to ``False``
       - Return ``False`` 
