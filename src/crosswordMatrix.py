import ctypes
import random

#TODO pep8

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

# instantiate C function interface
cfunctions = ctypes.CDLL(".\\lib\\cfunctions.so")
c_best_place_in_line = cfunctions.c_best_place_in_line
c_best_place_in_line.argtypes = [
    ctypes.c_int,       # height
    ctypes.c_int,       # width
    ctypes.c_char,      # direction ('v' or 'h')
    ctypes.c_char_p,    # word
    ctypes.c_char_p,    # matrixString
    ctypes.c_int,       # line
    ctypes.POINTER(ctypes.c_int),   # best offset
    ctypes.POINTER(ctypes.c_int),   # intersection count
    ]
c_best_place_in_line.restype = None
# end

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
                string += self.__matrix[i][j].getChar()# + " "
            string +="\n"
        return string

    def printM(self,wordWrapper = WORD_WRAPPER_CHAR, voidChar = VOID_CHAR):
        string = self.getMatrixString()
        string = string.replace(WORD_WRAPPER_CHAR,wordWrapper)
        string = string.replace(VOID_CHAR,voidChar)
        printStr = ""
        for i in range(0,len(string)):
            printStr += " " + string[i]
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

    def c_getBestPlaceInLine(self, line, direction, string):
        c_line = ctypes.c_int(line)
        c_height = ctypes.c_int(self.__HEIGHT)
        c_width = ctypes.c_int(self.__WIDTH)
        c_direction = ctypes.c_char(b'h' if direction==HORI_DIR else b'v')
        c_word = ctypes.create_string_buffer(string.encode('utf-8'))
        c_matrix_string = ctypes.create_string_buffer(self.getMatrixDescriptorStr().encode('utf-8'))
        c_best_offset = ctypes.c_int(-1)
        c_intersection_count = ctypes.c_int(-1)
        c_best_place_in_line(c_height,c_width,c_direction,c_word,c_matrix_string,c_line,ctypes.byref(c_best_offset),ctypes.byref(c_intersection_count))
        return c_best_offset.value, c_intersection_count.value


    def getBestPlaceInLine(self, line, direction, string):
        string = WORD_WRAPPER_CHAR + string + WORD_WRAPPER_CHAR
        #convert line to string
        lineStr = ""
        lineDirStr = ""
        if direction == HORI_DIR:
            for i in range(0,self.__WIDTH):
                lineStr += self.__matrix[i][line].getChar()
                lineDirStr += self.__matrix[i][line].getDir()
            lineStrLen = self.__WIDTH
        else:
            for i in range(0,self.__HEIGHT):
                lineStr += self.__matrix[line][i].getChar()
                lineDirStr += self.__matrix[line][i].getDir()
            lineStrLen = self.__HEIGHT
        stringLen = len(string)
        if stringLen > lineStrLen + 2: #doesn't fit at all
            return -1,-1
        #check if fits at the start
        intersections = 0
        bestOffset = -1
        bestOffsetIntersections = -1
        fits = True
        for i in range(0,stringLen-1):
            #check for vaccancy and for collisions
            if(i==lineStrLen and string[i+1]): #check if is last position
                continue
            if (string[i+1]!=lineStr[i] and lineStr[i]!=VOID_CHAR) or lineDirStr[i] == direction or lineDirStr[i] == BOTH_DIR:
                fits = False
                break
            #else
            if lineStr[i]!=VOID_CHAR and lineStr[i]!=WORD_WRAPPER_CHAR:
                intersections += 1
        if fits:
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
        for i in range(0,stringLen-2):
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
        string = WORD_WRAPPER_CHAR + string + WORD_WRAPPER_CHAR
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


    def getBestPlace(self,direction,string, c =False):
        bestPos = -1
        bestScore = -1
        bestOffset = -1
        if direction == HORI_DIR:
            dimension = self.__HEIGHT
        else:
            dimension = self.__WIDTH
        for i in range(0,dimension,2):
            if (c):
                offset, score = self.c_getBestPlaceInLine(i,direction,string)
            else:
                offset, score = self.getBestPlaceInLine(i,direction,string)
            #switch = HORI_DIR if direction == VERT_DIR else VERT_DIR
#            c_offset, c_score = self.c_getBestPlaceInLine(i,direction,string)
            if (bestScore<score):
                bestScore = score
                bestPos = i
                bestOffset = offset
        return bestOffset,bestPos,bestScore

    def placeWord(self,strWord, c = False):
        #strWord = WORD_WRAPPER_CHAR + strWord + WORD_WRAPPER_CHAR
        offset,pos,score = self.getBestPlace(self.__dirToggle,strWord, c)
        if(score==-1):
            return -1
        self.applyStrAtOffset(pos,self.__dirToggle,strWord,offset)
        # self.__dirToggle = VERT_DIR if self.__dirToggle == HORI_DIR else VERT_DIR
        if (self.__dirToggle == HORI_DIR):
            self.__dirToggle = VERT_DIR
        else:
            self.__dirToggle = HORI_DIR
        return score

    def placeWordDir(self,direction,strWord, c = False):
        #strWord = WORD_WRAPPER_CHAR + strWord + WORD_WRAPPER_CHAR
        offset,pos,score = self.getBestPlace(direction,strWord, c)
        if(score==-1):
            return -1
        self.applyStrAtOffset(pos,direction,strWord,offset)
        return score

    def sortDictionaryWithScores(self,dictionary, direction, c = False, kick = False):
        def getScore(str):
            offset,pos,score = self.getBestPlace(direction, str, c)
            return score
        dictionary.sort(key=len, reverse = True)
        dictAndScore = [[w,getScore(w)] for w in dictionary]
        dictAndScore.sort(key = lambda x : x[1], reverse = True)
        if kick:
            dictionary = [w[0] for w in dictAndScore if w[1]>=0]
        else:
            dictionary = [w[0] for w in dictAndScore]
        return dictionary
              

    def createCrossword(self,dictHori, dictVert, c = False):
        dictionaryH = dictHori.copy()
        dictionaryV = dictVert.copy()
        firstTime = True
        doneVertical = False
        doneHorizontal = False
        #find word with best score
        while(not doneVertical or not doneHorizontal):
            if (self.__dirToggle == HORI_DIR):
                dictionaryH = self.sortDictionaryWithScores(dictionaryH, HORI_DIR, c, kick = True)
                if dictionaryH:
                    sc = self.placeWordDir(HORI_DIR,dictionaryH[0], c)
                    dictionaryH.pop(0)
                else:
                    doneHorizontal = True
                if not firstTime and sc <= 0:
                    doneHorizontal = True
                self.__dirToggle = VERT_DIR

            # if direction is vertical
            else: 
                dictionaryV = self.sortDictionaryWithScores(dictionaryV, VERT_DIR, c, kick = True)
                if dictionaryV:
                    sc = self.placeWordDir(VERT_DIR,dictionaryV[0], c)
                    dictionaryV.pop(0)
                else:
                    doneVertical = True
                if not firstTime and sc <= 0:
                    doneVertical = True
                self.__dirToggle = HORI_DIR

            #end of while
            firstTime = False           



    def countIntersections(self): #TODO ver se vale otimizar
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

