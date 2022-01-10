import cv2
import os

class PathInfo:

    def __init__(self, absolutePath, name) -> None:
        self.absolutePath = absolutePath
        self.name = name

corruptedImage = cv2.imread("corruptedImage.png")

rootDirectory = os.getcwd() + "/midi"
urls = []
for gameName in os.listdir(rootDirectory):
    urls.append(PathInfo(rootDirectory + "/" + gameName, gameName))

if os.path.exists("errors2.log"):
    os.remove("errors2.log")
else:
    print("errors.log does not exist, generating")

for game in urls:
    numberOfImages = 0
    for gameFile in os.listdir(game.absolutePath):
        if gameFile[len(gameFile)-3:] != "png":
            continue
        numberOfImages += 1
        image = cv2.imread(game.absolutePath + "/" + gameFile)
        if corruptedImage.shape != image.shape:
            continue
        difference = cv2.subtract(corruptedImage, image)
        b, g, r = cv2.split(difference)

        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            with open("errors2.log", "a") as errorFile:
                errorFile.write("CORRUPTED IMAGES AT (sometimes gives false positive)::: "
                                + game.absolutePath + gameFile +"\n")
            break
    if numberOfImages == 0:
        with open("errors2.log", "a") as errorFile:
            errorFile.write("NO IMAGES AT::: " + game.absolutePath + "\n")

