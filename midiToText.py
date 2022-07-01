import py_midicsv as pm
import sys
import os

def logAnError(error):
    with open("errorsMidiConversion.log", "a") as f:
        f.write(str(error) + "\n")



def convertMidiFile(midiName):
    if midiName[-3:] != "mid" and midiName[-4:] != "midi":
        return
    print(midiName)

    try:
        csv_string = pm.midi_to_csv(midiName)
    except Exception as error:
        logAnError(error)
        return
    with open(midiName + ".txt", "w") as f:
        f.writelines(csv_string)

def convertMidiFolder(path):
    for midiName in os.listdir(path):
        convertMidiFile(path + "/" + midiName)

def convertMidiFolderOfFolders(path):
    for midiName in os.listdir(path):
        convertMidiFolder(path + "/" + midiName)


midiName = sys.argv[1]

mode = "file"

if(len(sys.argv) >= 3):
    mode = sys.argv[2]

if(mode == "file"):
    convertMidiFile(midiName)
elif(mode == "folder"):
    convertMidiFolder(midiName)
elif(mode == "ffolder"):
    convertMidiFolderOfFolders(midiName)

print("fin mode")
