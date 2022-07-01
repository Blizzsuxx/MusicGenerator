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
    # print("AAAA")
    with open(fin, "r") as fajl:
        channelInstrumentDictionary = {}
        lastTimestamp = 0
        currentTimestamp = 0
        for line in fajl.readlines():
            tokens = line.split(",")
            # print(tokens)
            lastTimestamp = currentTimestamp
            currentTimestamp = int(tokens[1])
            if currentTimestamp > lastTimestamp:
                wholeAssFile.append("wait-" + str(currentTimestamp - lastTimestamp))
            
            if tokens[2] == " Program_c":
                channelInstrumentDictionary[tokens[3]] = tokens[4].strip()
            elif tokens[2] == " Note_on_c":
                instrument = "n"
                if tokens[3] in channelInstrumentDictionary.keys():
                    instrument = channelInstrumentDictionary[tokens[3]]

                if tokens[5] != " 0":
                    wholeAssFile.append(tokens[3].strip() + DELIMETER + tokens[4].strip() + DELIMETER + tokens[5].strip()
                    + DELIMETER + instrument.strip() + DELIMETER + "d" )
                else:
                    for i in range(len(wholeAssFile)-1, -1, -1):
                        noteTokens = wholeAssFile[i].split(DELIMETER)
                        if noteTokens[0] == tokens[3].strip() and noteTokens[1] == tokens[4].strip():
                            noteTokens[4] = str(int(tokens[1]) - int(noteTokens[0]))
                        wholeAssFile[i] = DELIMETER.join(noteTokens)
                        break
    # print("AAAA")
    with open(fout, "w") as fajl:
        fajl.write(NOTE_DELIMETER.join(wholeAssFile))


def uncompress(fin, fout):
    lastTimestamp = 0
    with open(fin, "r") as fajl:
        priorityList = compressMidi.PriorityLinkedList()
        wholeAssFile = fajl.read()
        for line in wholeAssFile.split(NOTE_DELIMETER):
            if line.startswith('-'):
                line = line[1:]
            if line.endswith('-'):
                line = line[:-1]
            tokens = line.split(DELIMETER)
            # print(tokens)
            if len(tokens) == 2:
                lastTimestamp += int(tokens[1])
                continue
            if "wait" in tokens or len(tokens)!=5 or int(tokens[1]) >128: #error
                continue
            # print(tokens)



            if tokens[3] != "n":
                priorityList.add2(lastTimestamp, "1" + REGULAR_MIDI_DELIMETER + str(lastTimestamp) + REGULAR_MIDI_DELIMETER + "Program_c" + REGULAR_MIDI_DELIMETER +
                tokens[0] + REGULAR_MIDI_DELIMETER + tokens[3])

            priorityList.add2(lastTimestamp, "1" + REGULAR_MIDI_DELIMETER + str(lastTimestamp) + REGULAR_MIDI_DELIMETER +
            "Note_on_c" + REGULAR_MIDI_DELIMETER + tokens[0] + REGULAR_MIDI_DELIMETER + tokens[1] + REGULAR_MIDI_DELIMETER +
            tokens[2])


            if tokens[4] != 'd':
                priorityList.add2(lastTimestamp + int(tokens[4]), "1" + REGULAR_MIDI_DELIMETER + str(lastTimestamp + int(tokens[4]))
                 + REGULAR_MIDI_DELIMETER +
                "Note_on_c" + REGULAR_MIDI_DELIMETER + tokens[0] + REGULAR_MIDI_DELIMETER + tokens[1] + REGULAR_MIDI_DELIMETER +
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
            compress(path + "/" +fajl, os.path.curdir + "/smallTestDataset3/" + fajl)
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
    
    # path = "smallTestDataset2"
    # paths = os.listdir(path)
    # main(paths, path)
