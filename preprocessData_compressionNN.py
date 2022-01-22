from lib2to3.pgen2 import token
import os
import sys
import compressMidi

DELIMETER = "-"
NOTE_DELIMETER = " "
REGULAR_MIDI_DELIMETER = ", "
REGULAT_NOTE_MIDI_DELIMETER = "\n"

def compress(fin, fout):
    wholeAssFile = []
    print("AAAA")
    with open(fin, "r") as fajl:
        channelInstrumentDictionary = {}
        
        for line in fajl.readlines():
            tokens = line.split(",")

            if tokens[2] == " Program_c":
                channelInstrumentDictionary[tokens[3]] = tokens[4].strip()
            elif tokens[2] == " Note_on_c":
                instrument = "NONE"
                if tokens[3] in channelInstrumentDictionary.keys():
                    instrument = channelInstrumentDictionary[tokens[3]]

                if tokens[5] != " 0":
                    wholeAssFile.append(tokens[1].strip() + DELIMETER + tokens[3].strip() + DELIMETER + tokens[4].strip() + DELIMETER + tokens[5].strip()
                    + DELIMETER + instrument.strip() )
                else:
                    for i in range(len(wholeAssFile)-1, -1, -1):
                        noteTokens = wholeAssFile[i].split(DELIMETER)
                        if noteTokens[1] == tokens[3].strip() and noteTokens[2] == tokens[4].strip():
                            noteTokens.append(int(tokens[1]) - int(noteTokens[0]))
                        wholeAssFile[i] = DELIMETER.join(noteTokens)
                        break
    print("AAAA")
    with open(fout, "w") as fajl:
        fajl.write(NOTE_DELIMETER.join(wholeAssFile))


def uncompress(fin, fout):
    lastTimestamp = None
    with open(fin, "r") as fajl:
        priorityList = compressMidi.PriorityLinkedList()
        wholeAssFile = fajl.read()
        for line in wholeAssFile.split(NOTE_DELIMETER):
            tokens = line.split(DELIMETER)
            print(tokens)

            if len(tokens) >= 5 and tokens[4] != "NONE":
                priorityList.add2(int(tokens[0]), "1" + REGULAR_MIDI_DELIMETER + tokens[0] + REGULAR_MIDI_DELIMETER + "Program_c" + REGULAR_MIDI_DELIMETER +
                tokens[1] + REGULAR_MIDI_DELIMETER + tokens[4])

            priorityList.add2(int(tokens[0]), "1" + REGULAR_MIDI_DELIMETER + tokens[0] + REGULAR_MIDI_DELIMETER +
            "Note_on_c" + REGULAR_MIDI_DELIMETER + tokens[1] + REGULAR_MIDI_DELIMETER + tokens[2] + REGULAR_MIDI_DELIMETER +
            tokens[3])


            if len(tokens) == 6:
                priorityList.add2(int(tokens[0]) + int(tokens[5]), "1" + REGULAR_MIDI_DELIMETER + str(int(tokens[0]) + int(tokens[5]))
                 + REGULAR_MIDI_DELIMETER +
                "Note_on_c" + REGULAR_MIDI_DELIMETER + tokens[1] + REGULAR_MIDI_DELIMETER + tokens[2] + REGULAR_MIDI_DELIMETER +
                "0")

    with open(fout, "w") as fajl:
        fajl.write(compressMidi.BEGINNING_OF_THE_FILE)
        currentNode = priorityList.pop()
        firstTimestamp = int(currentNode.value.split(REGULAR_MIDI_DELIMETER)[1])
        while currentNode != None:
            noteSplit = currentNode.value.split(REGULAR_MIDI_DELIMETER)

            noteSplit[1] = str(int(noteSplit[1]) - firstTimestamp)
            lastTimestamp = noteSplit[1]
            fajl.write(REGULAR_MIDI_DELIMETER.join(noteSplit) + REGULAT_NOTE_MIDI_DELIMETER)
            currentNode = priorityList.pop()
        fajl.write("1" + REGULAR_MIDI_DELIMETER + lastTimestamp + REGULAR_MIDI_DELIMETER + "End_track\n" )
        fajl.write(compressMidi.END_OF_THE_FILE)

def main(paths, path):
    for i in range(len(paths)):
        fajl = paths[i]
        print(str(i) + " / " + str(len(paths)))
        try:
            compress(path + "/" +fajl, os.path.curdir + "/data5/" + fajl)
        except Exception as e:
            print(path + "/" + fajl)
            print(str(e))


if __name__ == "__main__":
    fin = sys.argv[1]
    fout = sys.argv[2]
    mode = sys.argv[3]
    print("AAAAAAA")
    if mode == "c":
        print("AAAAAAA")
        compress(fin, fout)
    elif mode == "u":
        uncompress(fin, fout)
    
    # path = "data4"
    # paths = os.listdir(path)
    # main(paths, path)
