import tensorflow as tf
import gpt_2_simple as gpt2

tf.compat.v1.reset_default_graph()

sess2 = gpt2.start_tf_sess()

gpt2.load_gpt2(sess2,run_name ="run1")
tekst = "wait-4 1-64-55-29-d wait-63 2-37-0-37-d 9-38-0-24-d wait-4 2-30-117-37-d 9-36-75-24-d wait-41 1-64-0-29-d wait-4 1-68-55-29-d wait-63 2-30-0-37-d 9-36-0-24-d wait-4 2-30-80-37-d 9-44-75-24-d wait-41 1-68-0-29-d wait-4 1-71-55-29-d wait-63 2-30-0-37-d 9-44-0-24-d wait-4 2-30-117-37-d 9-36-75-24-d wait-108 2-30-0-37-d 9-36-0-24-d wait-4 2-30-80-37-d 9-44-75-24-d wait-108 2-30-0-37-d 9-44-0-24-d wait-4 2-37-117-37-d 9-38-75-24-d wait-108 2-37-0-37-d 9-38-0-24-d wait-4 2-30-117-37-d 9-36-75-24-d wait-108 2-30-0-37-d 9-36-0-24-d wait-4 2-30-117-37-d 9-44-75-24-d wait-109 2-30-0-37-d 9-44-0-24-d wait-3 2-30-117-37-d 9-36-75-24-d wait-109 2-30-0-37-d 9-36-0-24-d wait-3 2-30-80-37-d 9-44-75-24-d wait-109 2-30-0-37-d 9-44-0-24-d wait-3 2-30-117-37-d 9-38-75-24-d wait-109 2-30-0-37-d 9-38-0-24-d wait-3 2-30-80-37-d 9-44-75-24-d wait-109 0-71-0-29-d 2-30-0-37-d 9-44-0-24-d wait-3 0-69-79-29-d 2-31-117-37-d 9-36-75-24-d wait-109"

wholeSong = tekst
for i in range(10):

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