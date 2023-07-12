import fileHandler
import algorythms
import crosswordMatrix
from defs import *
import copy
import os

def generateCrosswordsAndFiles(width, height, nOfCrossWordsToGenerate, minimumScore, dictionary, c = False):
    usedWords = fileHandler.readUsedWords()
    dictionary = [d for d in dictionary if d not in usedWords]
    # dictionary = dictionary[0:100] ##########DEBUG
    for i in range(0,nOfCrossWordsToGenerate):
        matrix = crosswordMatrix.Matrix(width,height)
        while (matrix.countIntersections()<minimumScore):
            matrix, usedWords = algorythms.lookAhead(width,height,dictionary,7, c)#LOOK_OVER_X_TOP_WORDS)
        matrix.printM(" "," ")
        usedWordsStr = ""
        for word in usedWords:
            usedWordsStr += word + '\n'
            dictionary.pop(dictionary.index(word))
        #create files
        matrixString = matrix.getMatrixString()
        offset = 0
        while(os.path.isfile(OUTPUT_PATH+"\crossword"+str(offset+i)+"\Descriptor.txt")): offset += 1
        fileHandler.saveString(matrix.getMatrixString(),OUTPUT_PATH+"\crossword"+str(i+offset)+"\Layout.txt")
        fileHandler.saveString(matrix.getDirectionsString(),OUTPUT_PATH+"\crossword"+str(i+offset)+"\Directions.txt")
        fileHandler.saveString(matrix.getMatrixDescriptorStr(),OUTPUT_PATH+"\crossword"+str(i+offset)+"\Descriptor.txt")
        fileHandler.saveString(usedWordsStr,OUTPUT_PATH+"\crossword"+str(i+offset)+"\Words.txt")


def findForever(width, height, nOfCrossWordsToGenerate, minimumScore, dictionary, c = False):
    
    usedWords = fileHandler.readUsedWords()
    for uw in usedWords:
        dictionary.pop(dictionary.index(uw))
    for i in range(0,nOfCrossWordsToGenerate):
        matrix = crosswordMatrix.Matrix(width,height)
        bestMatrix = matrix
        history = []
        historyMat = []
        while (True):
            matrix, usedWords = algorythms.lookAhead(width,height,dictionary,37, c)#LOOK_OVER_X_TOP_WORDS)
            history.append(matrix.countIntersections())
            historyMat.append(copy.deepcopy(matrix))
            if matrix.countIntersections() > bestMatrix.countIntersections():
                bestMatrix = matrix

#generateCrosswordsAndFiles(WIDTH, HEIGHT, CROSSWORDS_TO_GENERATE, 41, DICTIONARY_FILE_NAME)
if __name__=="__main__":
    dictionary = fileHandler.getDictionaries()

    generateCrosswordsAndFiles(width=WIDTH, height=HEIGHT, nOfCrossWordsToGenerate=15, minimumScore=37, dictionary=dictionary, c = True)


# readUsedWords()
