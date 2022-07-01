import os


startOfText = "<|startoftext|>\n"
# startOfText = ""
endOfText = "\n<|endoftext|>\n"

path = "all_of_the_data/"
paths = os.listdir(path)

tekst = ""

for i in range(len(paths)):
    if i%25 != 0:
        continue
    fajl = paths[i]
    print(str(i) + " / " + str(len(paths)))
    with open(path+ fajl, "r") as file:
        tekst += startOfText + file.read() + endOfText

with open("dataset.txt", "w") as file:
        file.write(tekst)