import random
import os
from defs import *

# WIDTH = 20
# HEIGHT = 30



def openDictionary(filename):
    dictionary = []
    #imports dictionary and sorts
    with open(filename) as file:
        dictionary = file.read().split('\n')
    rand = lambda a : random.random()
    dictionary.sort(key = rand)
    return dictionary

# dictionary = openDictionary(DICTIONARY_FILE_NAME)
#
# # Calls brute force algorythm
# if(ITERATIONS > 0):
#     bestMatrix,bestRatioMatrix,allScores = bruteForceAlgorythm(WIDTH,HEIGHT,dictionary)
#     print("Matrix with most intersections =",bestMatrix.countIntersections(),", ratio =",bestMatrix.getIntersectionRatio())
#     bestMatrix.printM()
#     print("Matrix with best ratio =",bestRatioMatrix.countIntersections(),", ratio =",bestRatioMatrix.getIntersectionRatio())
#     bestRatioMatrix.printM()
# # bestRatioMatrix.printDirections()
#
# # Calls look ahead algorythm
# if(LOOK_OVER_X_TOP_WORDS > 0):
#     matrix, usedWords = lookAheadAlgorythm(WIDTH,HEIGHT,dictionary)
#     matrix.printM()
#
def saveString(string, fileName):
    textFile = open(fileName, "w")
    n = textFile.write(string)
    textFile.close()

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
    return openDictionary(INPUT_PATH + "/" + DICTIONARY_FILE_NAME)
