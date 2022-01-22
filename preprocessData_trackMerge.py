import os
import sys
import mergeMidi.mergemid as mergeMidi

path = "Selenium/midi"
paths = os.listdir(path)
for i in range(len(paths)):
    dir = paths[i]
    for fajl in os.listdir(path + "/" + dir):
        if ".mid" in fajl:
            if not os.path.isdir(os.path.curdir + "/data2/" + dir):
                os.mkdir(os.path.curdir + "/data2/" + dir)
            print(str(i) + " / " + str(len(paths)))
            try:
                mergeMidi.main(path + "/" + dir + "/" +fajl, os.path.curdir + "/data2/" + dir + "/" + fajl)
            except Exception as e:
                print(dir + "/" + fajl)
                print(str(e))