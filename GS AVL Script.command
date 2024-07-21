#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User supplied variables
-------
    PATH: Path to the folder containing the input test file. Also used for exporting the result.
    INFILE: Name of the input WAV file.

Make sure Audacity is running and that mod-script-pipe is enabled
before running this script.
"""

import os
import sys
import time
import json

from pynput.keyboard import Key, Listener
from datetime import date

today = str(date.today())
os.system("open /Applications/Audacity.app")
time.sleep(10)


# Platform specific file name and file path.
# PATH is the location of files to be imported / exported.

#PATH = './'
PATH = "/Users/goodstewards/Library/CloudStorage/GoogleDrive-stewardssogood@gmail.com/.shortcut-targets-by-id/1lGE_0BZRjIAQ2qxxG7azMCqfUjGZg8Us/Recordings"
# while not os.path.isdir(PATH):
#     PATH = os.path.realpath(input('Path to test folder: '))
#     if not os.path.isdir(PATH):
#         print('Invalid path. Try again.')
# print('Test folder: ' + PATH)

"""
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
    EOL = '\r\n\0'
else:
    print("GSC AVL Script.command, running on linux or mac")
    PIPE_TO_AUDACITY = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    PIPE_FROM_AUDACITY = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'


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

TOPIPE = open(PIPE_TO_AUDACITY, 'w')
print("-- File to write to has been opened")
FROMPIPE = open(PIPE_FROM_AUDACITY, 'r')
print("-- File to read from has now been opened too\r\n")


def send_command(command):
    """Send a command to Audacity."""
    print("Send: >>> "+command)
    TOPIPE.write(command + EOL)
    TOPIPE.flush()


def get_response():
    """Get response from Audacity."""
    line = FROMPIPE.readline()
    result = ""
    while True:
        result += line
        line = FROMPIPE.readline()
        # print(f"Line read: [{line}]")
        if line == '\n':
            return result


def do_command(command):
    """Do the command. Return the response."""
    send_command(command)
    # time.sleep(0.1) # may be required on slow machines
    response = get_response()
    print("Rcvd: <<< " + response)
    return response






success = False

def play_record(key):
    """Import track and record to new track.
    Note that a stop command is not required as playback will stop at end of selection.
    """
    global success

    try: 
        if key.char == 'r':
            print("\nStart was pressed\n")
            do_command("Record2ndChoice")
        elif key.char == "s":
            print("\nStop was pressed\n")
            do_command("Stop")
            success = True
            return False
        elif key.char == "c":
            print("\nClear was pressed\n")
            do_command("Stop")
            do_command("SelectAll")
            do_command("RemoveTracks")
        elif key.char == "h":
            print("\nInputs:")
            print("r - start recording")
            print("s - stop recording, save, and upload")
            print("c - clear recording")
            print("h - help")
            print("esc - fail safe exit\n")
    except AttributeError:
        if key == Key.esc:
            do_command("Stop")
            do_command("SelectAll")
            do_command("RemoveTracks")
            return False
        pass


def export(filename):
    """Export the new track, and deleted both tracks."""
    do_command("Select: mode=Set")
    do_command("SelTrackStartToEnd")
    do_command(f"Export2: Filename={os.path.join(PATH, filename)} NumChannels=2")
    do_command("SelectAll")
    do_command("RemoveTracks")


def do_one_file(filename):
    """Run test with one input file only."""
    global success

    with Listener(on_press = play_record) as listener:
        listener.join()

    if success:
        export(filename)
        success = False


def music_pt_1():
    print("\nREADY FOR MUSIC PT 1")
    print("Enter \'h\' for help menu.\n")
    do_one_file("music_pt_1.mp3")

    file_name = PATH + "/music_pt_1.mp3"
    if os.path.exists(file_name):
        os.rename(file_name, PATH + "/" + today + " GS Music Pt 1.mp3")


def music_pt_2():
    print("\nREADY FOR MUSIC PT 2")
    print("Enter \'h\' for help menu.\n")
    do_one_file("music_pt_2.mp3")

    file_name = PATH + "/music_pt_2.mp3"
    if os.path.exists(file_name):
        os.rename(file_name, PATH + "/" + today + " GS Music Pt 2.mp3")


def sermon():
    print("\nREADY FOR SERMON")
    print("Enter \'h\' for help menu.\n")
    do_one_file("sermon.mp3")

    file_name = PATH + "/sermon.mp3"
    if os.path.exists(file_name):
        os.rename(file_name, PATH + "/gs " + today + ".mp3")


def starter():

    print("Please make sure that \'Export Audio\' is set to:")
    print("Format: MP3 Files")
    print("Quality: Insane, 320 kbps\n")

    print("Please make sure that \'Audio Setup\' is set to:")
    print("Playback Device: WING")
    print("Recording Device: WING")
    print("Recording Channels: 2 (Stereo)\n")

    print("Record: ")
    print("Inputs:")
    print("1 - music pt 1")
    print("2 - sermon")
    print("3 - music pt 2")
    print("a - all three\t <----")
    print("e - exit program\n")

    res = input()
    while True:
        if res == "a":
            music_pt_1()
            sermon()
            music_pt_2()
            break
        elif res == "1":
            music_pt_1()
            break
        elif res == "2":
            sermon()
            break
        elif res == "3":
            music_pt_2()
            break
        elif res == "e":
            break

        res = input()

    # close Audacity

    
starter()
