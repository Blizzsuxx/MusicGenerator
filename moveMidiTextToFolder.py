import os
import sys

path = "Selenium/midi"

for dir in os.listdir(path):
    for fajl in os.listdir(path + "/" + dir):
        if ".mid.txt" in fajl:
            os.replace(path + "/" + dir + "/" +fajl, os.path.curdir + "/data/" + dir + fajl)