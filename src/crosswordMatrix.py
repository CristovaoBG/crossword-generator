
import random

ITERATIONS = 0             #brute force tries, 0 to skip. (worst, but still cool)
LOOK_OVER_X_TOP_WORDS = 0   #look over algorythm, 0 to skip. (best)
#special characters (flags)
VOID_CHAR = '\''
WORD_WRAPPER_CHAR = '.'
#directions
NO_DIR = 'N'
VERT_DIR = '|'
HORI_DIR = '-'
BOTH_DIR = '+'

class Matrix:

    def getMatrixDescriptorStr(self):
        string = ""
        for w in self.words:
            string += str(w.x) + " " + str(w.y) + " " +  w.direction + " " + w.string + "\n"
        return string

    class Word:
        def __init__(self,word,x,y,direction):
            self.string = word
            self.x = x
            self.y = y
            self.direction = direction
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
        self.words = []
        #create empty matrix
        for column in range(0,width):
            matrixLine = []
            for row in range(0,height):
                matrixLine.append(self.Block())
            self.__matrix.append(matrixLine)

    def getCurrentDir(self):
        return self.__dirToggle

    def getMatrixString(self):
        string = ""
        for i in range(0,self.__HEIGHT):
            for j in range(self.__WIDTH):
                string += self.__matrix[j][i].getChar()# + " "
            string +="\n"
        # str.replace(VOID_CHAR," ")
        return string

    def printM(self):
        string = self.getMatrixString()
        # str.replace(VOID_CHAR," ")
        string = string.replace(WORD_WRAPPER_CHAR,' ')
        string = string.replace(VOID_CHAR,' ')
        printStr = ""
        for i in range(0,len(string)):
            printStr += string[i] + " "
        print(printStr)

    def getDirectionsString(self):
        str = ""
        for i in range(0,self.__HEIGHT):
            for j in range(self.__WIDTH):
                str += self.__matrix[j][i].getDir()
            str +="\n"
        return str
    #otimizavel essas duas (combinaveis como a printM e getMatrixString)
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

    def addWordToWordList(self,string,x,y,direction):
        if string[0] == WORD_WRAPPER_CHAR:
            string = string[1:]
            if direction == HORI_DIR:
                x = x + 1
            else:
                y = y + 1
        if string[-1] == WORD_WRAPPER_CHAR:
            string = string[:-1]
        self.words.append(self.Word(string,x,y,direction))

    def applyStrAtOffset(self,position,direction,string,offset):
        if offset == -1:
            string = string[1:]
            offset = 0
        if(direction == HORI_DIR):
            self.addWordToWordList(string,offset,position,direction)
            for i in range(0,len(string)):
                if (i+offset<self.__WIDTH):
                    self.__matrix[i+offset][position].set(string[i],HORI_DIR)
        else:
            self.addWordToWordList(string,position,offset,direction)
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

    def fillSpacesWithNoise(self):  # but.. why??
        for i in range(0,self.__WIDTH):
            for j in range(0,self.__HEIGHT):
                if self.__matrix[i][j].getChar() == VOID_CHAR or self.__matrix[i][j].getChar() == WORD_WRAPPER_CHAR:
                    self.__matrix[i][j].set(chr(int(random.random()*25 + 97)),NO_DIR)

