import os
import sys
import preprocessData_compressionNN_v2

path = "/media/user/games/Projects/MusicGenerator2/MusicGenerator/data4/"
paths = os.listdir(path)
for i in range(len(paths)):
    fajl = paths[i]
    print(str(i) + " / " + str(len(paths)))
    try:
        preprocessData_compressionNN_v2.compress(path+ fajl, os.path.curdir + "/all_of_the_data/" + fajl)
    except Exception as e:
        print("fail "+path + "/" + fajl)
        print(str(e))