import os
import sys
import datetime

from config import config

class Audacity():
    def __init__(self):
        self.PATH = config['local']['save_path']
        # os.system("open " + audacity_path)
        self.init_pipes()
        self.clear_audio()

    
    def init_pipes(self):
        while not os.path.isdir(self.PATH):
            self.PATH = os.path.realpath(input('Path to test folder: '))
            if not os.path.isdir(self.PATH):
                print('Invalid path. Try again.')
        print('Local save folder: ' + self.PATH)

        
        """
        Platform specific file name and file path.
        PATH is the location of files to be imported / exported.

        PATH = './'
        while not os.path.isdir(PATH):
            PATH = os.path.realpath(input('Path to test folder: '))
            if not os.path.isdir(PATH):
                print('Invalid path. Try again.')
        print('Test folder: ' + PATH)


        #INFILE = "testfile.wav"
        INFILE = ""
        while not os.path.isfile(os.path.join(PATH, INFILE)):
            INFILE = input('Name of input WAV file: ')
            # Ensure we have the .wav extension.
            INFILE = os.path.splitext(INFILE)[0] + '.wav'
            if not os.path.isfile(os.path.join(PATH, INFILE)):
                print(f"{os.path.join(PATH, INFILE)} not found. Try again.")
            else:
                print(f"Input file: {os.path.join(PATH, INFILE)}")
        # Remove file extension.
        INFILE = os.path.splitext(INFILE)[0]
        """
        
        # Platform specific constants
        if sys.platform == 'win32':
            print("GSC AVL Script.command, running on windows")
            PIPE_TO_AUDACITY = '\\\\.\\pipe\\ToSrvPipe'
            PIPE_FROM_AUDACITY = '\\\\.\\pipe\\FromSrvPipe'
            self.EOL = '\r\n\0'
        else:
            print("GSC AVL Script.command, running on linux or mac")
            PIPE_TO_AUDACITY = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
            PIPE_FROM_AUDACITY = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
            self.EOL = '\n'

        print("Write to  \"" + PIPE_TO_AUDACITY +"\"")
        if not os.path.exists(PIPE_TO_AUDACITY):
            print(""" ..does not exist.
            Ensure Audacity is running with mod-script-pipe.""")
            sys.exit()

        print("Read from \"" + PIPE_FROM_AUDACITY +"\"")
        if not os.path.exists(PIPE_FROM_AUDACITY):
            print(""" ..does not exist.
            Ensure Audacity is running with mod-script-pipe.""")
            sys.exit()

        print("-- Both pipes exist.  Good.")

        self.TOPIPE = open(PIPE_TO_AUDACITY, 'w')
        print("-- File to write to has been opened")
        self.FROMPIPE = open(PIPE_FROM_AUDACITY, 'r')
        print("-- File to read from has now been opened too\r\n")


    def send_command(self, command):
        """Send a command to Audacity."""
        print("Send: >>> "+command)
        self.TOPIPE.write(command + self.EOL)
        self.TOPIPE.flush()


    def get_response(self):
        """Get response from Audacity."""
        line = self.FROMPIPE.readline()
        result = ""
        while True:
            result += line
            line = self.FROMPIPE.readline()
            # print(f"Line read: [{line}]")
            if line == '\n':
                return result


    def do_command(self, command):
        """Do the command. Return the response."""
        self.send_command(command)
        # time.sleep(0.1) # may be required on slow machines
        response = self.get_response()
        print("Rcvd: <<< " + response)
        return response
    

    # Record command
    def record_audio(self):
        self.do_command("Record1stChoice")


    # Stop command
    def stop_audio(self):
        return self.do_command("Stop")


    # Save command
    def save_audio(self, filename):
        response = self.stop_audio()
        
        """Export track, and delete track."""
        self.do_command("Select: mode=Set")
        self.do_command("SelTrackStartToEnd")
        self.do_command("LoudnessNormalization")

        print(os.path.join(self.PATH, filename))
        response = self.do_command(f"Export2: Filename={os.path.join(self.PATH, filename)} NumChannels=2")
        if "BatchCommand finished: Failed!" in response:
            return False
        
        self.clear_audio()

        return True
    

    # Clear command
    def clear_audio(self):
        self.stop_audio()
        self.do_command("SelectAll")
        self.do_command("RemoveTracks")


    # Exit command
    def exit(self):
        self.do_command("Exit")
