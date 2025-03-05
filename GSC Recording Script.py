import sys
import time
import subprocess

from config import config
from send2trash import send2trash
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from Audacity import *
from GoogleCloud import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.audacity_service = Audacity()
        self.google_cloud_service = GoogleCloud()

        # Date
        self.date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        # Is there a recording?
        self.curr_recording_flag = False
        # Record or pause?
        self.record_state_flag = False
        # Enables 'Upload to Google Drive' button if there are local files to upload
        self.file_flag = False
        self.cross_seeds_flag = False

        self.init_UI()

    """ Start up ================================================================================================================================================================"""

    # Open
    # If there are files in local directory, notify user
    def check_local_directory(self):
        self.clean_directory()

        if self.check_directory():
            file_names = os.listdir(config['local']['save_path'])

            service = 'GSC'
            if 'CS' in file_names[0]:
                self.cross_seeds_flag = True
                service = 'Cross Seeds'

            self.create_warning_box("There are currently \'" + service + "\' files in the local directory:\n\n" + self.list_files_box() + "\nPlease check and clear local directory, or upload to Google Drive before recording.")
            
            if service == 'GSC':
                self.text_edit.insertPlainText("\'GSC\' Session\n")
                self.create_message_box("Continuing previous \'GSC\' session")
            else:
                self.cross_seeds_check_box.setCheckState(Qt.Checked, True)
            
            self.update_upload_state()
            self.cross_seeds_check_box.setEnabled(False)
        else:
            self.text_edit.insertPlainText("Default: \'GSC\' Session\n")

    """ Exit ================================================================================================================================================================"""

    # Close
    # 1. If there are files that have not been uploaded, notify user
    # 2. If there is a recording in process, notify user
    # Exits Audacity too
    # https://stackoverflow.com/questions/9249500/pyside-pyqt-detect-if-user-trying-to-close-window
    def closeEvent(self, event):
        self.clean_directory()
        self.check_directory()

        if self.file_flag:
            if self.user_prompt_box("Files in directory", "There are currently files in the local directory to be uploaded:\n\n" + self.list_files_box() + "\nWould you still like to exit?"):
                self.audacity_service.exit()
                event.accept()
            else:
                event.ignore()

        elif self.curr_recording_flag:
            if self.user_prompt_box("Recording", "There is currently a recording in process.\n\nWould you still like to exit?"):
                self.audacity_service.exit()
                event.accept()
            else:
                event.ignore()
        else:
            self.audacity_service.exit()
            event.accept()

    """ User Interface ================================================================================================================================================================"""

    # Initialize UI
    def init_UI(self):
        # Main Window
        self.setWindowTitle("Good Stewards Church Recording")
        self.setGeometry(0, 0, 385, 385)

        # Buttons
        self.record_button = QPushButton("Record" , self)
        self.pause_button = QPushButton("Pause", self)
        self.clear_button = QPushButton("Clear", self)
        self.save_button = QPushButton("Save", self)
        self.upload_button = QPushButton("Upload", self)
        self.local_button = QPushButton("Local Files", self)
        self.copy_button = QPushButton("Copy", self)

        self.record_button.setFixedSize(60, 45)
        self.pause_button.setFixedSize(60, 45)
        self.clear_button.setFixedSize(60, 45)
        self.save_button.setFixedSize(60, 45)
        self.upload_button.setFixedSize(100, 40)
        self.copy_button.setFixedSize(90, 30)
        self.local_button.setFixedSize(90, 30)

        self.record_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.pause_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.clear_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.save_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.upload_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.local_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.copy_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")

        # Default buttons on start up
        self.record_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.upload_button.setEnabled(False)
        self.local_button.setEnabled(True)
        self.copy_button.setEnabled(True)

        # Connect buttons to their respective functions
        self.record_button.clicked.connect(self.record)
        self.pause_button.clicked.connect(self.pause)
        self.clear_button.clicked.connect(self.clear)
        self.save_button.clicked.connect(self.save)
        self.upload_button.clicked.connect(self.upload)
        self.local_button.clicked.connect(self.open_directory)
        self.copy_button.clicked.connect(self.copy)

        # Cross Seeds Checkbox
        self.cross_seeds_check_box = QCheckBox('Cross Seeds', self)
        self.cross_seeds_check_box.stateChanged.connect(self.check_box_update)

        # Drop down menu
        # https://www.pythonguis.com/docs/qcombo_box/
        self.combo_box = QComboBox()
        self.combo_box.setFixedSize(250, 40)
        self.combo_box.addItems(['Music Pt. 1', 'Sermon', 'Music Pt. 2'])

        # Drop down menu editing
        self.combo_box.setEditable(True)
        self.combo_box.setInsertPolicy(3)

        # Text Editor to add messages
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFixedSize(343, 343)

        # Layout
        self.v_layout = QVBoxLayout()
        self.h_layout1 = QHBoxLayout()
        self.h_layout2 = QHBoxLayout()
        self.h_layout3 = QHBoxLayout()
        self.h_layout4 = QHBoxLayout()
        
        self.h_layout1.addWidget(self.cross_seeds_check_box)
        self.h_layout1.addWidget(self.combo_box)

        self.h_layout2.addWidget(self.record_button)
        self.h_layout2.addWidget(self.pause_button)
        self.h_layout2.addWidget(self.clear_button)
        self.h_layout2.addWidget(self.save_button)

        self.h_layout3.addWidget(self.text_edit)

        self.h_layout4.addWidget(self.local_button)
        self.h_layout4.addWidget(self.upload_button)
        self.h_layout4.addWidget(self.copy_button)

        self.v_layout.addLayout(self.h_layout1)
        self.v_layout.addLayout(self.h_layout2)
        self.v_layout.addLayout(self.h_layout3)
        self.v_layout.addLayout(self.h_layout4)

        container = QWidget()
        container.setLayout(self.v_layout)
        self.setCentralWidget(container)

    """ Button functions ================================================================================================================================================================"""

    # Start/Continue recording
    def record(self):
        self.text_edit.insertPlainText(str(datetime.datetime.now().strftime("%H:%M:%S")) + ": Record pressed\n")
        self.pause_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.record_button.setStyleSheet("background-color: yellowgreen; padding: 3px; border-radius: 5px;")

        self.disable_buttons()

        # Call Audacity 'record'
        self.audacity_service.record_audio()

        # There is now a recording in progress
        self.curr_recording_flag = True
        # In the 'record' state
        self.record_state_flag = True

        self.record_button.setEnabled(False)
        self.pause_button.setEnabled(True)

        self.update_record_state()
        self.update_upload_state()
        self.enable_local_files_copy()

    # Pause the recording
    def pause(self):
        self.text_edit.insertPlainText(str(datetime.datetime.now().strftime("%H:%M:%S")) + ": Pause pressed\n")
        self.record_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.pause_button.setStyleSheet("background-color: goldenrod; padding: 3px; border-radius: 5px;")

        self.disable_buttons()

        # Call Audacity 'stop'
        self.audacity_service.stop_audio()

        self.record_state_flag = False

        self.record_button.setEnabled(True)
        self.pause_button.setEnabled(False)

        self.update_record_state()
        self.update_upload_state()
        self.enable_local_files_copy()

    # Clear the recording
    def clear(self):
        self.text_edit.insertPlainText(str(datetime.datetime.now().strftime("%H:%M:%S")) + ": Clear pressed\n")
        self.record_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.pause_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.clear_button.setStyleSheet("background-color: indianred; padding: 3px; border-radius: 5px;")
        
        self.disable_buttons()

        if self.user_prompt_box("Clear Prompt", "Clear the recording?"):
            # Call Audacity 'clear'
            self.audacity_service.clear_audio()

            # There is now no recording in process
            self.curr_recording_flag = False

            self.record_button.setEnabled(True)
            self.pause_button.setEnabled(False)

            self.text_edit.insertPlainText(str(datetime.datetime.now().strftime("%H:%M:%S")) + ": Recording cleared\n")

        self.update_record_state()
        self.update_upload_state()
        self.enable_local_files_copy()

        self.clear_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")


    # Save to local disk, clear Audacity recording to prepare for next recording
    def save(self):
        self.text_edit.insertPlainText(str(datetime.datetime.now().strftime("%H.%M.%S")) + ": Save pressed\n")
        self.record_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.pause_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.save_button.setStyleSheet("background-color: dodgerblue; padding: 3px; border-radius: 5px;")

        self.disable_buttons()

        if self.user_prompt_box("Save Prompt", "Save current recording?"):
            text_name = self.combo_box.currentText()
            # Audacity does not recognize white spaces properly, so we use the combobox index for the file name and properly rename it after save
            indexed_name = str(self.combo_box.currentIndex()) + ".mp3"

            if self.audacity_service.save_audio(indexed_name):
                file_name = self.audacity_service.PATH + "/" + indexed_name

                # Renaming files
                service = 'GSC'
                if self.cross_seeds_flag:
                    service = 'CS'
                if os.path.exists(file_name):
                    os.rename(file_name, self.audacity_service.PATH + "/" + self.date + " " + str(datetime.datetime.now().strftime("%H.%M.%S")) + " " + service + " " + text_name + ".mp3")

                self.create_message_box(f"\'{text_name}\' saved successfully!")

                self.curr_recording_flag = False
                self.file_flag = True

                self.record_button.setEnabled(True)

                self.text_edit.insertPlainText(str(datetime.datetime.now().strftime("%H:%M:%S")) + ": \'" + text_name + "\' save successful\n")
            else:
                self.create_warning_box("File save failed.\nPlease restart program.")
                self.text_edit.insertPlainText(str(datetime.datetime.now().strftime("%H:%M:%S")) + ": \'" + text_name + "\' save failed\n")
        else:
            self.save_button.setEnabled(True)

            if not self.file_flag:
                self.cross_seeds_check_box.setEnabled(True)

        self.update_record_state()  
        self.update_upload_state()  
        self.enable_local_files_copy()

        self.save_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")


    # Upload to Google Drive
    def upload(self):
        self.text_edit.insertPlainText(str(datetime.datetime.now().strftime("%H:%M:%S")) + ": Upload pressed\n")
        self.record_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.pause_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
        self.upload_button.setStyleSheet("background-color: dodgerblue; padding: 3px; border-radius: 5px;")

        self.disable_buttons()

        self.clean_directory()
        if not self.check_directory():
            self.create_warning_box("No files in local directory.\nUnlocking current session.")

            if self.cross_seeds_check_box.isChecked():
                self.text_edit.insertPlainText("Starting \'Cross Seeds\' Session\n")
            else:
                self.text_edit.insertPlainText("Starting \'GSC\' Session\n")

            self.record_button.setEnabled(True)
            self.cross_seeds_check_box.setEnabled(True)

        elif self.curr_record_prompt_box():
            if self.user_prompt_box("Google Drive Prompt", "Upload to Google Drive?") and self.user_prompt_box("Local files", "The following files will be uploaded:\n\n" + self.list_files_box() + "\nWould you like to continue?"):
                self.clean_directory()
                self.check_directory()
                
                # Google Drive Upload
                self.google_cloud_service.exec()

                # Messenger text
                self.text_edit.clear()
                if self.cross_seeds_flag:
                    self.text_edit.insertPlainText("Cross Seeds " + self.date + "\n\n")
                else:
                    self.text_edit.insertPlainText("GSC " + self.date + "\n\n")

                self.get_links(self.google_cloud_service.get_music_links())
                self.get_links(self.google_cloud_service.get_sermon_links())
                self.get_links(self.google_cloud_service.get_misc_links())
                self.google_cloud_service.clear_links()

                # Clear local recordings directory to trash
                self.empty_directory()

                self.create_message_box("Google Drive upload was successful!")

                # There are no files in local directory
                self.file_flag = False

                self.cross_seeds_check_box.setEnabled(True)

            self.record_button.setEnabled(True)
        
        self.update_record_state()
        self.update_upload_state()
        self.enable_local_files_copy()

        self.upload_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")


    # Copy text on textedit to clipboard
    def copy(self):
        self.text_cursor = self.text_edit.textCursor()

        self.text_edit.selectAll()
        self.text_edit.copy()
        
        self.text_cursor.clearSelection()
        self.text_edit.setTextCursor(self.text_cursor)

    def open_directory(self):
        path = config['local']['save_path']
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Directory not found: {path}")
            subprocess.run(["open", path])
        except FileNotFoundError as e:
            print("Uh oh\n")

    """ Helper functions ================================================================================================================================================================"""

    # GSC/Cross Seeds check box
    def check_box_update(self, state, start_up = None):
        if state == self.cross_seeds_check_box.isChecked():
            self.cross_seeds_flag = False
            self.google_cloud_service.cross_seeds(False)
            self.text_edit.insertPlainText("Starting \'GSC\' Session\n")
            self.create_message_box("New Session: \'GSC\'\n")
        else:
            self.cross_seeds_flag = True
            self.google_cloud_service.cross_seeds(True)
            self.text_edit.insertPlainText("Starting \'Cross Seeds\' Session\n")
            if start_up:
                self.create_message_box("Continuing previous \'Cross Seeds\'\n")
            else:
                self.create_message_box("New Session: \'Cross Seeds\'\n")


    # Disables all buttons
    def disable_buttons(self):
        self.cross_seeds_check_box.setEnabled(False)
        self.record_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.local_button.setEnabled(False)
        self.upload_button.setEnabled(False)
        self.copy_button.setEnabled(False)


    # If there is a recording present, enable Clear, Save buttons; restore Record/Pause states
    def update_record_state(self):
        if self.curr_recording_flag:
            self.clear_button.setEnabled(True)
            self.save_button.setEnabled(True)

            if self.record_state_flag:
                self.record_button.setStyleSheet("background-color: yellowgreen; padding: 3px; border-radius: 5px;")
                self.pause_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
                self.record_button.setEnabled(False)
                self.pause_button.setEnabled(True)
            else:
                self.record_button.setStyleSheet("background-color: grey; padding: 3px; border-radius: 5px;")
                self.pause_button.setStyleSheet("background-color: goldenrod; padding: 3px; border-radius: 5px;")
                self.record_button.setEnabled(True)
                self.pause_button.setEnabled(False)


    # If there are files in the local_recordings directory, enable Upload button
    def update_upload_state(self):
        if self.file_flag:
            self.upload_button.setEnabled(True)


    # Enable local files and copy buttons
    def enable_local_files_copy(self):
        self.local_button.setEnabled(True)
        self.copy_button.setEnabled(True)

    
    # Pre-Upload list files to user
    def list_files_box(self):
        file_names = os.listdir(config['local']['save_path'])
        file_names.sort()

        temp = ""
        for file_name in file_names:
            if ".mp3" in file_name:
                temp += file_name + "\n"

        return temp


    # Iterates through given list and appends letter to differentiate same title files 
    def get_links(self, links):
        start_index = 24
        if self.cross_seeds_flag:
            start_index = 23

        length = len(links)
        # If empty, do nothing
        if not length:
            return
        
        if length > 1:
            ascii_upper = 'abcdefghijklmnopqrstuvwxyz'

            # time complexity: O(N), space complexity: O(1)
            count = 0
            for i in range(len(links)):
                file = links[i]
                mp3 = len(file['name']) - 4
                title = file['name'][start_index:mp3]
                link = file['link']

                # Edge case: first element
                if i == 0:
                    # Check element title after this element only
                    if file['name'][start_index:] == links[i + 1]['name'][start_index:]:
                        self.text_edit.insertPlainText(title + '-' + ascii_upper[count] + ": " + link + "\n\n")
                        count += 1
                    else:
                        self.text_edit.insertPlainText(title + ": " + link + "\n\n")
                # Edge case: last element
                elif i == len(links) - 1:
                    # Check element title before this element only
                    if file['name'][start_index:] == links[i - 1]['name'][start_index:]:
                        self.text_edit.insertPlainText(title + '-' + ascii_upper[count] + ": " + link + "\n\n")
                    else:
                        self.text_edit.insertPlainText(title + ": " + link + "\n\n")
                else:
                    # Check element title before to see if current element title is new
                    if file['name'][start_index:] != links[i - 1]['name'][start_index:]:
                        count = 0
                    # Check element title after current element
                    if file['name'][start_index:] == links[i + 1]['name'][start_index:] or file['name'][start_index:] == links[i - 1]['name'][start_index:]:
                        self.text_edit.insertPlainText(title + '-' + ascii_upper[count] + ": " + link + "\n\n")
                        count += 1
                    else:
                        self.text_edit.insertPlainText(title + ": " + link + "\n\n")
        else:
            file = links[0]
            mp3 = len(file['name']) - 4
            title = file['name'][start_index:mp3]
            link = file['link']
            self.text_edit.insertPlainText(title + ": " + link + "\n\n")


    def clean_directory(self):
        for root, dirs, files in os.walk(self.audacity_service.PATH):
            for f in files:
                if "mp3" not in f:
                    send2trash(os.path.join(root, f))
            for d in dirs:
                send2trash(os.path.join(root, d))


    def empty_directory(self):
        for root, dirs, files in os.walk(self.audacity_service.PATH):
            for f in files:
                send2trash(os.path.join(root, f))
            for d in dirs:
                send2trash(os.path.join(root, d))


    def check_directory(self):
        file_names = os.listdir(config['local']['save_path'])
        if len(file_names):
            self.file_flag = True
            return True
        else:
            self.file_flag = False
            return False


    """ Message Boxes ================================================================================================================================================================"""
    
    # Startup message
    def open_message_box(self):
        QMessageBox.information(self, "Initial Setup", "Initial Setup:\n\nExport Audio:\nFormat: MP3 Files\nQuality: 320 kbps\n\nAudio Setup:\nPlayback Device: WING\nRecording Device: WING\nRecording Channels: 2 (Stereo)\n")


    # Success message
    def create_message_box(self, message):
        QMessageBox.information(self, "Success", message)
    

    # Failure message
    def create_warning_box(self, message):
        QMessageBox.warning(self, "Warning", message)


    # User prompt message
    def user_prompt_box(self, text, informative_text):
        reply = QMessageBox.question(self, text, informative_text, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False
        

    # Upload when recording message
    def curr_record_prompt_box(self):
        if self.curr_recording_flag:
            return self.user_prompt_box("Recording", "There is a recording in progress.\n\nWould you like to continue?")
        else:
            return True

""" Main ================================================================================================================================================================"""

def main():
    os.system("open " + config['audacity']['app_path'])

    # UI
    time.sleep(8)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.check_local_directory()
    window.open_message_box()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()