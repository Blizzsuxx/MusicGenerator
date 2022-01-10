from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import threading
from LinkedList import LinkedList
import sys


class PathInfo:

    def __init__(self, absolutePath, name) -> None:
        self.absolutePath = absolutePath
        self.name = name


fp = webdriver.FirefoxProfile()
threadRunning = True

fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", os.getcwd() + "/midi")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/png")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpg")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")


def threadThatMovesFiles(dictionaryList, rootDirectory):
    global threadRunning
    failureCounter = 0
    while threadRunning:
        time.sleep(10)
        for gameTitleToMidiFileDictionary in dictionaryList:

            while not gameTitleToMidiFileDictionary.isEmpty():
                node = gameTitleToMidiFileDictionary.pop()
                print("moving: " + rootDirectory[:len(rootDirectory)-5] + "/" +
                      node.value + " to: " + rootDirectory + "/" + node.key + "/" + node.value)
                try:
                    os.replace(rootDirectory[:len(
                        rootDirectory)-5] + "/" + node.value, rootDirectory + "/" + node.key + "/" + node.value)
                except(OSError) as e:
                    print("FAILED TO MOVE")
                    print(e)
                    with open("errors.log", "a") as errorFile:
                        errorFile.write("FAILED TO MOVE: " + rootDirectory[:len(
                            rootDirectory)-5] + "/" + node.value + " to: " + rootDirectory + "/" + node.key + "/" + node.value + "\n")


def getHighQualityImage(image, songName, gameTitleToMidiFileDictionary):
    newDriver = webdriver.Firefox(firefox_profile=fp)

    newDriver.get(image.find_element_by_tag_name("a").get_property("href"))
    time.sleep(2)
    newDriver.find_element_by_tag_name("img").screenshot(
        gameName.name + " - " + songName[:len(songName)-4] + str(i) + ".png")
    gameTitleToMidiFileDictionary.add2(
        gameName.name, gameName.name + " - " + songName[:len(songName)-4] + str(i) + ".png")
    newDriver.close()


def threadThatScrapes(gameTitleToMidiFileDictionary, gameNames):
    global fp
    driver = webdriver.Firefox(firefox_profile=fp)
    for gameName in gameNames:
        # driver.get("https://www.giantbomb.com/search/?q=" +
        #            gameName.name + " " + songName[:len(songName)-4])
        driver.get("https://www.giantbomb.com/search/?q=" +
                   gameName.name)
        gameLink = driver.find_element_by_class_name("media")
        gameLink.click()
        driver.get(driver.current_url + "images/")
        time.sleep(2)

        images = driver.find_elements("tag name", "figure")

        for i in range(len(images)):
            image = images[i]
            image.screenshot(
                gameName.name  + " - square" + str(i) + ".png")
            gameTitleToMidiFileDictionary.add2(
                gameName.name, gameName.name + " - square" + str(i) + ".png")
            #getHighQualityImage(image, songName, gameTitleToMidiFileDictionary)

    driver.close()
    print("THREAD DONE!")

def start(rootDirectory, urls, numOfThreads):
    

    if os.path.exists("errors.log"):
        os.remove("errors.log")
    else:
        print("errors.log does not exist, generating")

    

    dictionaryList = [None] * numOfThreads
    for i in range(numOfThreads):
        dictionaryList[i] = LinkedList()


    increment = len(urls) // numOfThreads
    number = increment
    lastNumber = 0
    for i in range(numOfThreads):
        thread = threading.Thread(target=threadThatScrapes, args=(
            dictionaryList[i], urls[lastNumber:number]))
        lastNumber = number
        number += increment
        thread.start()
        time.sleep(2)

    thread = threading.Thread(target=threadThatMovesFiles, args=(dictionaryList, rootDirectory))
    thread.start()

if __name__ == "__main__":
    rootDirectory = os.getcwd() + "/midi"
    urls = []
    numOfThreads = int(sys.argv[1])
    for gameName in os.listdir(rootDirectory):
        urls.append(PathInfo(rootDirectory + "/" + gameName, gameName))
    start(rootDirectory, urls, numOfThreads)