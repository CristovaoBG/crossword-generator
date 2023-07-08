import fileHandler
import algorythms
import crosswordMatrix
from defs import *
import copy

def generateCrosswordsAndFiles(width, height, nOfCrossWordsToGenerate, minimumScore, dictionary, c = False):
    
    usedWords = fileHandler.readUsedWords()
    for uw in usedWords:
        dictionary.pop(dictionary.index(uw))
    # dictionary = dictionary[0:100] ##########DEBUG
    for i in range(0,nOfCrossWordsToGenerate):
        matrix = crosswordMatrix.Matrix(width,height)
        while (matrix.countIntersections()<minimumScore):
            matrix, usedWords = algorythms.lookAhead(width,height,dictionary,10, c)#LOOK_OVER_X_TOP_WORDS)
        matrix.printM()
        usedWordsStr = ""
        for word in usedWords:
            usedWordsStr += word + '\n'
            dictionary.pop(dictionary.index(word))
        #create files
        matrixString = matrix.getMatrixString()
        fileHandler.saveString(matrix.getMatrixString(),OUTPUT_PATH+"\crossword"+str(i)+"\Layout.txt")
        fileHandler.saveString(matrix.getDirectionsString(),OUTPUT_PATH+"\crossword"+str(i)+"\Directions.txt")
        fileHandler.saveString(matrix.getMatrixDescriptorStr(),OUTPUT_PATH+"\crossword"+str(i)+"\Descriptor.txt")
        fileHandler.saveString(usedWordsStr,OUTPUT_PATH+"\crossword"+str(i)+"\Words.txt")


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
            matrix, usedWords = algorythms.lookAhead(width,height,dictionary,10, c)#LOOK_OVER_X_TOP_WORDS)
            history.append(matrix.countIntersections())
            historyMat.append(copy.deepcopy(matrix))
            if matrix.countIntersections() > bestMatrix.countIntersections():
                bestMatrix = matrix

#generateCrosswordsAndFiles(WIDTH, HEIGHT, CROSSWORDS_TO_GENERATE, 41, DICTIONARY_FILE_NAME)
if __name__=="__main__":
    dictionary = fileHandler.getDictionaries()
    findForever(width=WIDTH, height=HEIGHT, nOfCrossWordsToGenerate=CROSSWORDS_TO_GENERATE, minimumScore=39, dictionary=dictionary, c = True)
# readUsedWords()
