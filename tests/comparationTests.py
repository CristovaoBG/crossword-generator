import os
import sys

currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(currentDir, '../src'))
import fileHandler
import copy
import random
import crosswordMatrix
from defs import *


def lookAhead(width,height,dictionaryOrig,lookOverXTopWords):

    def calculatesFutureScore(dictionary, word, matrix):
        newMatrix = copy.deepcopy(matrix)
        c_newMatrix = copy.deepcopy(matrix)
        newMatrix.placeWord(word)
        c_newMatrix.placeWord(word, c = True)
        descr = newMatrix.getMatrixDescriptorStr()
        c_descr = c_newMatrix.getMatrixDescriptorStr()
        if(c_descr != descr):
            print("ERRO, INCONSISTENCIA:\n Matriz:")
            newMatrix.printM()
            print("c_Matriz:")
            c_newMatrix.printM()
        newDictionary = dictionary.copy()
        #remove current word of new dictionary
        newDictionary.pop(newDictionary.index(word))
        newMatrix.sortDictionaryWithScores(newDictionary)
        newMatrix.createCrossword(newDictionary)
        # score = newMatrix.getIntersectionRatio()
        score = newMatrix.countIntersections()
        return score, newMatrix

    dictionary = dictionaryOrig.copy()
    print("dictionary size:",len(dictionary))
    matrix = crosswordMatrix.Matrix(width,height)
    usedWords = []
    #otimizavel (proprimeira palavra testada varias vezes)
    while True:
        print("looking for next word...")
        matrix.sortDictionaryWithScores(dictionary)
        bestFutureMatrix = matrix
        bestWord = dictionary[0]
        bestScore = -1
        score,futureMatrix = calculatesFutureScore(dictionary, dictionary[0], matrix)
        if ((len(dictionary[0]) == 3 and score==2)) or (len(dictionary[0]) == 2 and score==1):
            bestScore = score
            bestWord = dictionary[0]
            #bestFutureMatrix = copy.deepcopy(futureMatrix)
        else:
            for word in dictionary[0:lookOverXTopWords]:
                # calcula o melhor score futuro das cinco melhores palavras atuais
                score,futureMatrix = calculatesFutureScore(dictionary, word, matrix)
                print(score,"-> score of",word)

                if score > bestScore:
                    bestScore = score
                    bestWord = word
                    #bestFutureMatrix = copy.deepcopy(futureMatrix)
                #adds a little bit of impredictibility
                elif score == bestScore and random.random() >= 0.5:
                    bestScore = score
                    bestWord = word
                    #bestFutureMatrix = copy.deepcopy(futureMatrix)

        if bestScore < 0:
            break
        sc = matrix.placeWord(bestWord)
        if sc == -1:
            break
        print("selected word:",bestWord,". future score:",bestScore)
        usedWords.append(bestWord)
        #remove current word out of the dictionary
        dictionary.pop(dictionary.index(bestWord))
    return matrix, usedWords

def generateCrosswordsAndFiles(width, height, nOfCrossWordsToGenerate, minimumScore, dictionary, c = False):
    
    usedWords = fileHandler.readUsedWords()
    for uw in usedWords:
        dictionary.pop(dictionary.index(uw))
    # dictionary = dictionary[0:100] ##########DEBUG
    for i in range(0,nOfCrossWordsToGenerate):
        matrix = crosswordMatrix.Matrix(width,height)
        while (matrix.countIntersections()<minimumScore):
            matrix, usedWords = lookAhead(width,height,dictionary,3)#LOOK_OVER_X_TOP_WORDS)
        matrix.printM()
        usedWordsStr = ""
        for word in usedWords:
            usedWordsStr += word + '\n'
            dictionary.pop(dictionary.index(word))
        # #create files
        # matrixString = matrix.getMatrixString()
        # fileHandler.saveString(matrix.getMatrixString(),OUTPUT_PATH+"\crossword"+str(i)+"\Layout.txt")
        # fileHandler.saveString(matrix.getDirectionsString(),OUTPUT_PATH+"\crossword"+str(i)+"\Directions.txt")
        # fileHandler.saveString(matrix.getMatrixDescriptorStr(),OUTPUT_PATH+"\crossword"+str(i)+"\Descriptor.txt")
        # fileHandler.saveString(usedWordsStr,OUTPUT_PATH+"\crossword"+str(i)+"\Words.txt")


#generateCrosswordsAndFiles(WIDTH, HEIGHT, CROSSWORDS_TO_GENERATE, 41, DICTIONARY_FILE_NAME)
if __name__=="__main__":
    dictionary = fileHandler.getDictionaries()
    generateCrosswordsAndFiles(width=WIDTH, height=HEIGHT, nOfCrossWordsToGenerate=CROSSWORDS_TO_GENERATE, minimumScore=39, dictionary=dictionary, c = True)
# readUsedWords()