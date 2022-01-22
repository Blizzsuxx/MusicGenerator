import os
import sys
import compressMidi

path = "data3"
paths = os.listdir(path)
for i in range(len(paths)):
    fajl = paths[i]
    print(str(i) + " / " + str(len(paths)))
    try:
        compressMidi.stripFile(path + "/" +fajl, os.path.curdir + "/data4/" + fajl)
    except Exception as e:
        print(path + "/" + fajl)
        print(str(e))