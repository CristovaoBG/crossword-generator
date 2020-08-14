import random
import copy

WIDTH = 13
HEIGHT = 20
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

    def printM(self):
        str = ""
        for i in range(0,self.__HEIGHT):
            for j in range(self.__WIDTH):
                str += self.__matrix[j][i].getChar() + " "
            str +="\n"
        print(str)

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
            return
        self.applyStrAtOffset(pos,self.__dirToggle,strWord,offset)
        # self.__dirToggle = VERT_DIR if self.__dirToggle == HORI_DIR else VERT_DIR
        if (self.__dirToggle == HORI_DIR):
            self.__dirToggle = VERT_DIR
        else:
            self.__dirToggle = HORI_DIR

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
            for i in range(0,len(words)):
                strWord = WORD_WRAPPER_CHAR + words[i] + WORD_WRAPPER_CHAR
                offset,pos,score = self.getBestPlace(self.__dirToggle,strWord)
                if bestScore < score or (score == bestScore and len(strWord) > len(bestStr)):
                    bestOffset = offset
                    bestPos = pos
                    bestScore = score
                    bestId = i
                    bestStr = strWord
            if not firstTime and bestScore <= 0:
                return
            self.applyStrAtOffset(bestPos,self.__dirToggle,bestStr,bestOffset)
            words.pop(bestId)
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
        return intersections/noIntersection

    def fillSpacesWithNoise(self):
        for i in range(0,self.__WIDTH):
            for j in range(0,self.__HEIGHT):
                if self.__matrix[i][j].getChar() == VOID_CHAR or self.__matrix[i][j].getChar() == WORD_WRAPPER_CHAR:
                    self.__matrix[i][j].set(chr(int(random.random()*25 + 97)),NO_DIR)

dictionary = []
#imports dictionary
with open("enem.txt") as file:
    dictionary = file.read().split('\n')

invLen = lambda a : 1/(len(a)+1)
rand = lambda a : random.random()
dictionary.sort(key = rand)
# dictionary = dictionary[0:20000]
# matrix.createCrossword(dictionary)
# for word in dictionary:
#     matrix.placeWord(word)

mostIntersections = -1
bestRatio = -1
emptyMatrix = Matrix(WIDTH,HEIGHT)
bestMatrix = emptyMatrix
bestRatioMatrix = emptyMatrix
#brute forces matrix with most intersections and best ratio
for i in range(0,1):
    dictionary.sort(key = rand)
    newMat = Matrix(WIDTH,HEIGHT)
    newMat.createCrossword(dictionary)
    totIntersections = newMat.countIntersections()
    ratio = newMat.getIntersectionRatio()
    print(i,totIntersections,ratio)
    if (mostIntersections < totIntersections):
        bestMatrix = copy.deepcopy(newMat)
        mostIntersections = totIntersections
    if (bestRatio < ratio):
        bestRatioMatrix = copy.deepcopy(newMat)
        bestRatio = ratio

print("bestMatrix: intersections =",bestMatrix.countIntersections(),", ratio =",bestMatrix.getIntersectionRatio())
bestMatrix.printM()
print("bestRatioMatrix: intersections =",bestRatioMatrix.countIntersections(),", ratio =",bestRatioMatrix.getIntersectionRatio())
bestRatioMatrix.printM()
bestRatioMatrix.printDirections()
bestRatioMatrix.fillSpacesWithNoise()
bestRatioMatrix.printM()



import pdb; pdb.set_trace()
