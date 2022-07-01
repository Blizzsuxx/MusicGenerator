import tensorflow as tf
import gpt_2_simple as gpt2

tf.compat.v1.reset_default_graph()

sess2 = gpt2.start_tf_sess()

gpt2.load_gpt2(sess2,run_name ="run1")
tekst = "wait-4 0-45-79-39-d wait-161 0-45-0-39-d wait-3 0-47-79-39-d wait-162 0-47-0-39-d wait-3 1-77-79-81-d 1-72-79-81-d 0-48-79-39-d wait-161 0-48-0-39-d wait-4 0-53-79-39-d wait-161 1-72-0-81-d 1-77-0-81-d 0-53-0-39-d wait-3 9-57-79-n-d 9-44-79-n-d 9-36-79-n-d 1-83-79-81-d 0-35-79-39-d wait-79 9-36-0-n-d 9-57-0-n-d 9-44-0-n-d 1-83-0-81-d wait-3 1-83-79-81-d wait-79 1-83-0-81-d 0-35-0-39-d wait-4 9-44-79-n-d 1-83-79-81-d 0-35-79-39-d wait-79 9-44-0-n-d 1-83-0-81-d wait-3 9-44-79-n-d 1-83-79-81-d wait-79 9-44-0-n-d 1-83-0-81-d 0-35-0-39-d wait-3 9-44-79-n-d 9-38-79-n-d 1-79-79-81-d 0-43-79-39-d wait-79 9-38-0-n-d 9-44-0-n-d 1-79-0-81-d wait-4 1-79-79-81-d wait-78 1-79-0-81-d 0-43-0-39-d wait-4 9-44-79-n-d 1-79-79-81-d 0-35-79-39-d wait-79 9-44-0-n-d 1-79-0-81-d wait-3 1-79-79-81-d wait-79 1-79-0-81-d 0-35-0-39-d wait-3 9-44-79-n-d 9-36-79-n-d 1-76-79-81-d 0-35-79-39-d wait-79 9-44-0-n-d 9-36-0-n-d 1-76-0-81-d wait-4 1-76-79-81-d wait-79 1-76-0-81-d 0-35-0-39-d wait-3 9-44-79-n-d 1-76-79-81-d 0-43-79-39-d wait-79 9-44-0-n-d 1-76-0-81-d wait-3 9-44-79-n-d 1-76-79-81-d wait-79 9-44-0-n-d 1-76-0-81-d 0-43-0-39-d wait-4 9-44-79-n-d 9-38-79-n-d 1-72-79-81-d 0-35-79-39-d wait-78 9-38-0-n-d 9-44-0-n-d 1-72-0-81-d wait-4 1-72-79-81-d wait-79"

wholeSong = tekst
for i in range(20):

    t=gpt2.generate(sess2,
                temperature=0.7,
                top_k=0,
                nsamples=1,
                batch_size=1,
                length=1000,
                prefix=tekst,
                truncate="<|endoftext|>",
                include_prefix=True, 
                sample_delim=' ',
                return_as_list=True)[0]
    wholeSong += t[len(tekst):]
    tekst = t[len(tekst)//3:]
    print("------------------------------------------------------------\n")
    print(wholeSong)
    print("------------------------------------------------------------\n")

print("******************************************************************")
print(wholeSong)
print("******************************************************************")

with open("encodedSong.txt", "w") as song:
    song.write(wholeSong)


import preprocessData_compressionNN_v2

preprocessData_compressionNN_v2.uncompress("encodedSong.txt", "decodedSong.txt")

import py_midicsv as pm

midiName = "decodedSong.txt"
midi_object = pm.csv_to_midi(midiName)

# Save the parsed MIDI file to disk
with open("convertedSong.mid", "wb") as output_file:
    midi_writer = pm.FileWriter(output_file)
    midi_writer.write(midi_object)