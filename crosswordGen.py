import random
import copy
import statistics

DICTIONARY_FILE_NAME = "dictionary.txt"
# WIDTH = 20
# HEIGHT = 30
WIDTH = 14
HEIGHT = 14
ITERATIONS = 1           #brute force tries, 0 to skip. (worst, but still cool)
LOOK_OVER_X_TOP_WORDS = 5  #look over algorythm, 0 to skip. (best)
#special characters (flags)
VOID_CHAR = '\''
WORD_WRAPPER_CHAR = '.'
#directions
NO_DIR = 'N'
VERT_DIR = '|'
HORI_DIR = '-'
BOTH_DIR = '+'

class Matrix:
    class Block:
        def __init__(self):
            self.__letter = VOID_CHAR
            self.__direction = NO_DIR
        def set(self,character,direction):
            self.__letter = character
            if (character == WORD_WRAPPER_CHAR):
                self.__direction = NO_DIR
            elif (self.__direction == NO_DIR):
                self.__direction = direction
            else:
                self.__direction = BOTH_DIR
        def getChar(self):
            return self.__letter
        def getDir(self):
            return self.__direction

    def __init__(self, width,height):
        self.__WIDTH = width
        self.__HEIGHT = height
        self.__matrix = []
        self.__dirToggle = VERT_DIR
        #create empty matrix
        for column in range(0,width):
            matrixLine = []
            for row in range(0,height):
                matrixLine.append(self.Block())
            self.__matrix.append(matrixLine)

    def getCurrentDir(self):
        return self.__dirToggle

    def printM(self):
        string = ""
        for i in range(0,self.__HEIGHT):
            for j in range(self.__WIDTH):
                string += self.__matrix[j][i].getChar() + " "
            string +="\n"
        # str.replace(VOID_CHAR," ")
        string = string.replace(WORD_WRAPPER_CHAR,' ')
        string = string.replace(VOID_CHAR,' ')
        print(string)

    def printDirections(self):
        str = ""
        for i in range(0,self.__HEIGHT):
            for j in range(self.__WIDTH):
                str += self.__matrix[j][i].getDir() + " "
            str +="\n"
        print(str)

    def setChar(self,char,posx,posy):
        self.__matrix[posy][posx].set(char,NO_DIR)

    def getBestPlaceInLine(self, line, direction, string):
        #convert line to string
        lineStr = ""
        lineDirStr = ""
        if direction == HORI_DIR:
            for i in range(0,self.__WIDTH):
                lineStr += self.__matrix[i][line].getChar()
                lineDirStr += self.__matrix[i][line].getDir();
            lineStrLen = self.__WIDTH
        else:
            for i in range(0,self.__HEIGHT):
                lineStr += self.__matrix[line][i].getChar()
                lineDirStr += self.__matrix[line][i].getDir();
            lineStrLen = self.__HEIGHT
        stringLen = len(string)
        if stringLen > lineStrLen + 1: #doesn't fit at all
            return -1,-1
        #check if fits at the start
        intersections = 0
        bestOffset = -1
        bestOffsetIntersections = -1
        fits = True
        for i in range(0,stringLen-1):
            #check for vaccancy and for collisions
            if (string[i+1]!=lineStr[i] and lineStr[i]!=VOID_CHAR) or lineDirStr[i] == direction or lineDirStr[i] == BOTH_DIR:
                fits = False
                break
            #else
            if lineStr[i]!=VOID_CHAR and lineStr[i]!=WORD_WRAPPER_CHAR:
                intersections += 1
        if fits == True:
            bestOffset = -1
            bestOffsetIntersections = intersections
            #check if fits at middle
        offset = 0
        while offset + stringLen <= lineStrLen:
            #compare every character
            fits = True
            intersections = 0
            for i in range(0,stringLen):
                #check for vaccancy and for collisions
                if (string[i]!=lineStr[i+offset] and lineStr[i+offset]!=VOID_CHAR) or lineDirStr[i+offset] == direction or lineDirStr[i+offset] == BOTH_DIR:
                    fits = False
                    break
                #else
                if lineStr[i+offset]!=VOID_CHAR and lineStr[i+offset]!=WORD_WRAPPER_CHAR:
                    intersections += 1
            if fits == True:
                if intersections > bestOffsetIntersections:
                    bestOffset = offset
                    bestOffsetIntersections = intersections
            offset += 1
        #check if fits at end
        fits = True
        intersections = 0
        for i in range(0,stringLen-1):
            #check for vaccancy and for collisions
            if (string[i]!=lineStr[i+offset] and lineStr[i+offset]!=VOID_CHAR) or lineDirStr[i+offset] == direction or lineDirStr[i+offset] == BOTH_DIR:
                fits = False
                break
            #else
            if lineStr[i+offset]!=VOID_CHAR and lineStr[i+offset]!=WORD_WRAPPER_CHAR:
                intersections += 1
        if fits == True:
            if intersections > bestOffsetIntersections:
                bestOffset = offset
                bestOffsetIntersections = intersections
        return bestOffset,bestOffsetIntersections

    def applyStrAtOffset(self,position,direction,string,offset):
        if offset == -1:
            string = string[1:]
            offset = 0
        if(direction == HORI_DIR):
            for i in range(0,len(string)):
                if (i+offset<self.__WIDTH):
                    self.__matrix[i+offset][position].set(string[i],HORI_DIR)
        else:
             for i in range(0,len(string)):
                 if (i+offset<self.__HEIGHT):
                     self.__matrix[position][i+offset].set(string[i],VERT_DIR)

    def getBestPlace(self,direction,string):
        bestPos = -1
        bestScore = -1
        bestOffset = -1
        if direction == HORI_DIR:
            dimension = self.__HEIGHT
        else:
            dimension = self.__WIDTH
        for i in range(0,dimension,2):
            offset, score = self.getBestPlaceInLine(i,direction,string)
            if (bestScore<score):
                bestScore = score
                bestPos = i
                bestOffset = offset
        return bestOffset,bestPos,bestScore

    def placeWord(self,strWord):
        strWord = WORD_WRAPPER_CHAR + strWord + WORD_WRAPPER_CHAR
        offset,pos,score = self.getBestPlace(self.__dirToggle,strWord)
        if(score==-1):
            return -1
        self.applyStrAtOffset(pos,self.__dirToggle,strWord,offset)
        # self.__dirToggle = VERT_DIR if self.__dirToggle == HORI_DIR else VERT_DIR
        if (self.__dirToggle == HORI_DIR):
            self.__dirToggle = VERT_DIR
        else:
            self.__dirToggle = HORI_DIR
        return score

    def placeWordDir(self,direction,strWord):
        strWord = WORD_WRAPPER_CHAR + strWord + WORD_WRAPPER_CHAR
        offset,pos,score = self.getBestPlace(direction,strWord)
        if(score==-1):
            return -1
        self.applyStrAtOffset(pos,direction,strWord,offset)
        # self.__dirToggle = VERT_DIR if self.__dirToggle == HORI_DIR else VERT_DIR
        return score

    def sortDictionaryWithScores(self,dictionary):
        def getScore(str):
            offset,pos,score = self.getBestPlace(self.__dirToggle,WORD_WRAPPER_CHAR+str+WORD_WRAPPER_CHAR)
            return score
        dictionary.sort(key=len, reverse = True)
        dictionary.sort(key=getScore, reverse = True)
        # print(dictionary[0:10])

    def createCrossword(self,dictionary):
        words = dictionary.copy()
        firstTime = True
        #find word with best score
        while(True):
            bestOffset = -1
            bestPos = -1
            bestScore = -1
            bestId = -1
            bestStr = ""
            self.sortDictionaryWithScores(words)
            sc = self.placeWordDir(self.__dirToggle,words[0])
            if not firstTime and sc <= 0:
                return
            # self.applyStrAtOffset(bestPos,self.__dirToggle,words[0],bestOffset)
            words.pop(0)
            # self.__dirToggle = VERT_DIR if self.__dirToggle == HORI_DIR else VERT_DIR
            if (self.__dirToggle == HORI_DIR):
                self.__dirToggle = VERT_DIR
            else:
                self.__dirToggle = HORI_DIR
            firstTime = False


    def countIntersections(self):
        intersections = 0
        for i in range(0,self.__WIDTH):
            for j in range(0,self.__HEIGHT):
                if self.__matrix[i][j].getDir() == BOTH_DIR:
                    intersections += 1
        return intersections

    def getIntersectionRatio(self):
        intersections = 0
        noIntersection = 0
        for i in range(0,self.__WIDTH):
            for j in range(0,self.__HEIGHT):
                if self.__matrix[i][j].getDir() == BOTH_DIR:
                    intersections += 1
                elif self.__matrix[i][j].getDir() == VERT_DIR or self.__matrix[i][j].getDir() == HORI_DIR:
                    noIntersection += 1
        if (noIntersection+intersections == 0):
            return -1
        return intersections/noIntersection#(noIntersection+intersections)

    def fillSpacesWithNoise(self):
        for i in range(0,self.__WIDTH):
            for j in range(0,self.__HEIGHT):
                if self.__matrix[i][j].getChar() == VOID_CHAR or self.__matrix[i][j].getChar() == WORD_WRAPPER_CHAR:
                    self.__matrix[i][j].set(chr(int(random.random()*25 + 97)),NO_DIR)


def bruteForceAlgorythm(width,height,dictionary):
    mostIntersections = -1
    bestRatio = -1
    emptyMatrix = Matrix(width,height)
    bestMatrix = emptyMatrix
    bestRatioMatrix = emptyMatrix
    #brute forces matrix with most intersections and best ratio
    scores = []
    # import pdb; pdb.set_trace()
    for i in range(0,ITERATIONS):
        dictionary.sort(key = rand)
        newMat = Matrix(width,height)
        newMat.createCrossword(dictionary)
        totIntersections = newMat.countIntersections()
        ratio = newMat.getIntersectionRatio()
        scores.append(ratio)
        print("iteration:",i,"total of intersections:",totIntersections,"intersection to letter ratio:",ratio)
        if (mostIntersections < totIntersections):
            bestMatrix = copy.deepcopy(newMat)
            mostIntersections = totIntersections
        if (bestRatio < ratio):
            bestRatioMatrix = copy.deepcopy(newMat)
            bestRatio = ratio
    return bestMatrix,bestRatioMatrix,scores

def lookAheadAlgorythm(width,height,dictionary):

    def calculatesFutureScore(dictionary, word, matrix):
        newMatrix = copy.deepcopy(matrix)
        newMatrix.placeWord(word)
        newDictionary = dictionary.copy()
        #remove current word of new dictionary
        newDictionary.pop(newDictionary.index(word))
        newMatrix.sortDictionaryWithScores(newDictionary)
        newMatrix.createCrossword(newDictionary)
        # score = newMatrix.getIntersectionRatio()
        score = newMatrix.countIntersections()
        return score, newMatrix

    print("dictionary size:",len(dictionary))
    matrix = Matrix(width,height)
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
            bestFutureMatrix = copy.deepcopy(futureMatrix)
        else:
            for word in dictionary[0:LOOK_OVER_X_TOP_WORDS]:
                # calcula o melhor score futuro das cinco melhores palavras atuais
                score,futureMatrix = calculatesFutureScore(dictionary, word, matrix)
                print(score,": score of",word)

                if score > bestScore:
                    bestScore = score
                    bestWord = word
                    bestFutureMatrix = copy.deepcopy(futureMatrix)
        if bestScore < 0:
            break
        sc = matrix.placeWord(bestWord)
        if sc == -1:
            break
        print("selected word:",bestWord,". future score:",bestScore)
        usedWords.append(bestWord)
        #remove current word of the dictionary
        dictionary.pop(dictionary.index(bestWord))
    return matrix, usedWords


dictionary = []
#imports dictionary and sorts
with open(DICTIONARY_FILE_NAME) as file:
    dictionary = file.read().split('\n')
rand = lambda a : random.random()
dictionary.sort(key = rand)
# dictionary = dictionary [0:100]
# Calls brute force algorythm
bestMatrix,bestRatioMatrix,allScores = bruteForceAlgorythm(WIDTH,HEIGHT,dictionary)
print("Matrix with most intersections =",bestMatrix.countIntersections(),", ratio =",bestMatrix.getIntersectionRatio())
bestMatrix.printM()
print("Matrix with best ratio =",bestRatioMatrix.countIntersections(),", ratio =",bestRatioMatrix.getIntersectionRatio())
bestRatioMatrix.printM()
# bestRatioMatrix.printDirections()

# Calls look ahead algorythm
if(LOOK_OVER_X_TOP_WORDS > 0):
    matrix, usedWords = lookAheadAlgorythm(WIDTH,HEIGHT,dictionary)
    matrix.printM()
