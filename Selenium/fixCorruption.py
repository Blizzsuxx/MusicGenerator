import os
import scrapImages


class PathInfo:

    def __init__(self, absolutePath, name) -> None:
        self.absolutePath = absolutePath
        self.name = name


rootDirectory = os.getcwd() + "/midi"
urls = []
with open("errors2.log", "r") as errorFile:
    for line in errorFile.readlines():
        if line[0] == "C":
            print(line.split('::: '))
            absolutePath = line.split('::: ')[1][:-1]
            gameName = absolutePath.split('/')[-1]
            urls.append(PathInfo(absolutePath, gameName))


scrapImages.start(rootDirectory, urls, 1)