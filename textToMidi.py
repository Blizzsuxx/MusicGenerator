import os
import sys
import py_midicsv as pm


# Parse the CSV output of the previous command back into a MIDI file
midiName = sys.argv[1]
midi_object = pm.csv_to_midi(midiName)

# Save the parsed MIDI file to disk
with open("example_converted.mid", "wb") as output_file:
    midi_writer = pm.FileWriter(output_file)
    midi_writer.write(midi_object)