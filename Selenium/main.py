from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import threading
from LinkedList import LinkedList
import sys



def threadThatMovesFiles():
    global threadRunning
    failureCounter = 0
    while threadRunning:
        time.sleep(10)
        for gameTitleToMidiFileDictionary in dictionaryList:

            if gameTitleToMidiFileDictionary.isEmpty():
                failureCounter += 1
                if failureCounter >= 10:
                    threadRunning = False

            while not gameTitleToMidiFileDictionary.isEmpty():
                node = gameTitleToMidiFileDictionary.pop()
                print("moving: " + rootDirectory + "/" + node.value + " to: " + rootDirectory + "/" + node.key + "/" + node.value)
                try:
                    os.replace(rootDirectory + "/" + node.value, rootDirectory + "/" + node.key + "/" + node.value)
                except(OSError) as e:
                    print("FAILED TO MOVE")
                    print(e)
                    with open("errors.log", "a") as errorFile:
                        errorFile.write("FAILED TO MOVE: " + rootDirectory + "/" + node.value + " to: " + rootDirectory + "/" + node.key + "/" + node.value + "\n")
                    
            


def threadThatScrapes(gameTitleToMidiFileDictionary, urls):
    global fp
    driver = webdriver.Firefox(firefox_profile=fp)
    for url in urls:
        driver.get(url)
        newElements = driver.find_elements("tag name", "a")
        gameTitle = None
        previousLink = newElements[2]
        for downloadLink in newElements[2:]:
            print(downloadLink.text)
            if "Comment" not in downloadLink.text and "Comment" not in previousLink.text:
                gameTitle = previousLink.text
                if "/" in gameTitle:
                    gameTitle = gameTitle.replace('/', ' ')
                if "." in gameTitle:
                    gameTitle = gameTitle.replace('.', ' ')
                    
                try:
                    os.mkdir(rootDirectory + "/" + gameTitle)
                except:
                    print("folder " + rootDirectory + "/" + gameTitle + " already exists")

            previousLink = downloadLink
            if "Comment" not in downloadLink.text:
                fileName = downloadLink.get_property("href").split('/')[-1]
                if fileName =="":
                    continue
                if "%" in fileName:
                    tokens = fileName.split('%')
                    fileName = tokens[0]
                    print("TOKENS: ", tokens)

                    for i in range(1, len(tokens)):
                        token = tokens[i]
                        print("TOKEN", token, len(token))
                        tempValue = tokens[i]=bytearray.fromhex(token[0:2]).decode()
                        fileName += tempValue + token[2:]
                
                print("adding: " + fileName)
                downloadLink.click()
                gameTitleToMidiFileDictionary.add2(gameTitle, fileName)
    print("THREAD DONE!")





rootDirectory = os.getcwd() + "/midi"

try:
    os.mkdir(rootDirectory)
except:
    print("folder midi already exists")

if os.path.exists("errors.log"):
  os.remove("errors.log")
else:
  print("errors.log does not exist, generating")

threadRunning = True

numOfThreads = int(sys.argv[1])

dictionaryList = [None] * numOfThreads
for i in range(numOfThreads):
    dictionaryList[i] = LinkedList()



fp = webdriver.FirefoxProfile()


fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", os.getcwd() + "/midi")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/midi")


driver = webdriver.Firefox(firefox_profile=fp)
driver.get("https://www.vgmusic.com/")
listOfElements = driver.find_elements("tag name", "a")
foundTheElements = False
urls = []
for element in listOfElements:
    print(element.text)
    if element.text == "NES":
        foundTheElements = True
    if element.text == "Comedy & Memes":
        break
    if foundTheElements:
        urls.append(element.get_property("href"))


with open("urls.txt", "w") as file:
    for line in urls:
        file.write(line+"\n")


driver.close()


increment = len(urls) // numOfThreads
number = increment
lastNumber = 0
for i in range(numOfThreads):
    thread = threading.Thread(target=threadThatScrapes, args=(dictionaryList[i], urls[lastNumber:number]))    
    lastNumber = number
    number+= increment
    thread.start()
    time.sleep(2)

thread =threading.Thread(target=threadThatMovesFiles)
thread.start()