from audioop import add
from heapq import merge
import sys
import os


class Node:
    def __init__(self, key, value) -> None:
        self._next = None
        self.key = key
        self.value = value
        self._previous = None

    def next(self):
        return self._next


class PriorityLinkedList:

    def __init__(self) -> None:
        self.head = None
        self.tail = self.head

    def pop(self) -> None:
        if not self.head is None:
            returnValue = self.head
            self.head = self.head._previous
            if self.head is None:
                self.tail = None
            return returnValue

    def add(self, node):
        if not self.tail is None:
            if self.tail.key <= node.key:
                node._next = self.tail
                self.tail._previous = node
                self.tail = node
            else:
                currentNode = self.tail
                previousNode = currentNode
                while currentNode.key > node.key:
                    previousNode = currentNode
                    currentNode = currentNode._next
                previousNode._next = node
                node._previous = previousNode
                node._next = currentNode
                currentNode._previous = node

        else:
            self.head = node
            self.tail = node

        return node

    def add2(self, key, value):
        return self.add(Node(key, value))

    def get(self, key):
        currentNode = self.tail
        if not currentNode is None:
            while key < currentNode.key:
                currentNode = currentNode._next
            if key == currentNode.key:
                return currentNode
            else:
                return self.add2(key, "")
        else:
            return self.add2(key, "")

    def isEmpty(self):
        return self.head is None


FILTERED_LIST = [" Time_signature", " Key_signature", " MIDI_port", " End_of_file", " Copyright_t", " Text_t",
                 " Sequencer_specific", " Channel_prefix", " Pitch_bend_c", " Cue_point_t", " Marker_t", " Device_name_t",
                 " SMPTE_offset"]

ALLOW_LIST = [" Header", " Start_track\n", " Title_t", " Program_c", " Note_on_c", " End_track\n"]
DEFAULT_TEMPO_VALUE = 500000.00
DEFAULT_HEADER_DIVISION = 480.00
DEFAULT_VOLUME = 127.00
BEGINNING_OF_THE_FILE = '''0, 0, Header, 0, 1, 480
1, 0, Start_track
1, 0, Title_t, ""
'''
END_OF_TRACK = "1, , End_track"

END_OF_THE_FILE = '0, 0, End_of_file'


def mergeFile(dictionary):
    theWholeAssFile = ""
    while True:
        currentNode = dictionary.pop()
        if currentNode is None:
            break
        theWholeAssFile += currentNode.value

    return theWholeAssFile + END_OF_THE_FILE


def stripFile(fileName, output):
    odnosTempo = 1
    odnosDivision = 1

    timeDictionary = PriorityLinkedList()
    channelVolume = {}

    with open(fileName, "r") as fajl:
        for line in fajl.readlines():
            tokens = line.split(",")
            
            if tokens[2] == " Tempo":
                value = float(tokens[3])
                odnosTempo = value / DEFAULT_TEMPO_VALUE
                continue
            if tokens[2] == " Control_c":
                if tokens[4] == " 7" or tokens[4] == " 39":
                    channelVolume[tokens[3]] = float(
                        tokens[5]) / DEFAULT_VOLUME
                    pass
                continue
            if tokens[2] == " Header":

                odnosDivision = DEFAULT_HEADER_DIVISION / float(tokens[5])
                tokens[5] = " " + str(int(DEFAULT_HEADER_DIVISION)) + "\n"

            if odnosTempo != 1:
                tokens[1] = " " + \
                    str(round(float(tokens[1]) * odnosTempo * odnosDivision))

            if tokens[2] == " Note_on_c":
                channelCoeficient = 1
                if not (tokens[3] in channelVolume.keys()):
                    channelVolume[tokens[3]] = 1
                else:
                    channelCoeficient = channelVolume[tokens[3]]
                tokens[5] = " " + \
                    str(round(float(tokens[5]) * channelCoeficient)) + "\n"
            if tokens[2] == " Note_off_c":
                tokens[2] = " Note_on_c"
                tokens[5] = " 0\n"
            #print(tokens)
            if tokens[2] in ALLOW_LIST:
                timeDictionary.get(int(tokens[1])).value += ",".join(tokens)
    theWholeAssFile = mergeFile(timeDictionary)
    with open(output, "w") as fajl:
        fajl.write(theWholeAssFile)


if __name__ == "__main__":
    fileName = sys.argv[1]
    output = sys.argv[2]
    stripFile(fileName, output)
