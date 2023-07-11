import random
import os
from defs import *

# WIDTH = 20
# HEIGHT = 30

def readDictionaryFiles(path):
    output = []
    for fileName in os.listdir(path):
        filePath = os.path.join(path, fileName)
        if os.path.isfile(filePath):
            with open(filePath, 'r') as file:
                for line in file:
                    words = line.split()
                    if(words):
                        output.append(words[0])
    return output    

def openDictionary(filename):
    dictionary = []
    #imports dictionary and sorts
    with open(filename) as file:
        dictionary = file.read().split('\n')
    rand = lambda a : random.random()
    dictionary.sort(key = rand)
    return dictionary

def saveString(string, fileName):
    os.makedirs(os.path.dirname(fileName), exist_ok = True)
    with open(fileName, "w") as textFile:
        n = textFile.write(string)
    return n

def readUsedWords():
    currentPath = os. getcwd()
    currentPath += "\\crosswords"
    filesPath = []
    for r, d, f in os.walk(currentPath):
        for file in f:
            if '.txt' in file:
                filesPath.append(os.path.join(r, file))
    #get all words files only
    wordsFilesPaths = []
    for path in filesPath:
        fileName = path.split('\\')[-1]
        if(fileName.find("Words") > 0):
            wordsFilesPaths.append(path)
            print(fileName)
    #readAllWords
    usedWords = []
    for f in wordsFilesPaths:
        with open(f) as file:
             words = file.read().split('\n')
        for word in words:
            if (len(word)>0):
                usedWords.append(word)
    return usedWords

def getDictionaries():
    #return openDictionary(INPUT_PATH + "/" + DICTIONARY_FILE_NAME)
    return readDictionaryFiles(".\\data\\input")
