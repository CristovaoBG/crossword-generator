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

    def get_matrix_descriptor_str(self):
        string = ""
        for w in self.words:
            string += f"{w.x} {w.y} {w.direction} {w.string}\n"
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
        def get_char(self):
            return self.__letter
        def get_dir(self):
            return self.__direction

    def __init__(self, width,height):

        self.__WIDTH = width
        self.__HEIGHT = height
        self.__matrix = []
        self.__dir_toggle = VERT_DIR
        self.words = []
        #create empty matrix
        for column in range(0,width):
            matrix_line = []
            for row in range(0,height):
                matrix_line.append(self.Block())
            self.__matrix.append(matrix_line)
    def get_current_dir(self):
        return self.__dir_toggle

    def get_matrix_string(self):
        string = ""
        for i in range(0,self.__HEIGHT):
            for j in range(self.__WIDTH):
                string += self.__matrix[i][j].get_char()# + " "
            string +="\n"
        return string

    def printM(self,word_wrapper = WORD_WRAPPER_CHAR, void_char = VOID_CHAR):
        string = self.get_matrix_string()
        string = string.replace(WORD_WRAPPER_CHAR,word_wrapper)
        string = string.replace(VOID_CHAR,void_char)
        print_str = ""
        for i in range(0,len(string)):
            print_str += " " + string[i]
        print(print_str)

    def get_directions_string(self):
        str = ""
        for i in range(0,self.__HEIGHT):
            for j in range(self.__WIDTH):
                str += self.__matrix[j][i].getDir()
            str +="\n"
        return str
    #otimizavel essas duas (combinaveis como a printM e getMatrixString)
    def print_directions(self):
        str = ""
        for i in range(0,self.__HEIGHT):
            for j in range(self.__WIDTH):
                str += self.__matrix[j][i].get_dir() + " "
            str +="\n"
        print(str)

    def set_char(self,char,posx,posy):
        self.__matrix[posy][posx].set(char,NO_DIR)

    def c_get_best_place_in_line(self, line, direction, string):
        c_line = ctypes.c_int(line)
        c_height = ctypes.c_int(self.__HEIGHT)
        c_width = ctypes.c_int(self.__WIDTH)
        c_direction = ctypes.c_char(b'h' if direction==HORI_DIR else b'v')
        c_word = ctypes.create_string_buffer(string.encode('utf-8'))
        c_matrix_string = ctypes.create_string_buffer(
            self.get_matrix_descriptor_str().encode('utf-8'))
        c_best_offset = ctypes.c_int(-1)
        c_intersection_count = ctypes.c_int(-1)
        c_best_place_in_line(c_height,
                             c_width,
                             c_direction,
                             c_word,
                             c_matrix_string,
                             c_line,
                             ctypes.byref(c_best_offset),
                             ctypes.byref(c_intersection_count)
                             )
        return c_best_offset.value, c_intersection_count.value


    def get_best_place_in_line(self, line, direction, string):
        string = WORD_WRAPPER_CHAR + string + WORD_WRAPPER_CHAR
        #convert line to string
        line_str = ""
        line_dir_str = ""
        if direction == HORI_DIR:
            for i in range(0,self.__WIDTH):
                line_str += self.__matrix[i][line].get_char()
                line_dir_str += self.__matrix[i][line].get_dir()
            line_str_len = self.__WIDTH
        else:
            for i in range(0,self.__HEIGHT):
                line_str += self.__matrix[line][i].get_char()
                line_dir_str += self.__matrix[line][i].get_dir()
            line_str_len = self.__HEIGHT
        string_len = len(string)
        if string_len > line_str_len + 2: #doesn't fit at all
            return -1,-1
        #check if fits at the start
        intersections = 0
        best_offset = -1
        best_offset_intersections = -1
        fits = True
        for i in range(0,string_len-1):
            #check for vaccancy and for collisions
            if(i==line_str_len and string[i+1]): #check if is last position
                continue
            if ((string[i+1]!=line_str[i] and line_str[i]!=VOID_CHAR) 
                    or line_dir_str[i] == direction 
                    or line_dir_str[i] == BOTH_DIR):
                fits = False
                break
            #else
            if line_str[i]!=VOID_CHAR and line_str[i]!=WORD_WRAPPER_CHAR:
                intersections += 1
        if fits:
            best_offset = -1
            best_offset_intersections = intersections
            #check if fits at middle
        offset = 0
        while offset + string_len <= line_str_len:
            #compare every character
            fits = True
            intersections = 0
            for i in range(0,string_len):
                #check for vaccancy and for collisions
                if ((string[i]!=line_str[i+offset] and line_str[i+offset]!=VOID_CHAR) 
                        or line_dir_str[i+offset] == direction 
                        or line_dir_str[i+offset] == BOTH_DIR):
                    fits = False
                    break
                #else
                if (line_str[i+offset]!=VOID_CHAR 
                        and line_str[i+offset]!=WORD_WRAPPER_CHAR):
                    intersections += 1
            if fits == True:
                if intersections > best_offset_intersections:
                    best_offset = offset
                    best_offset_intersections = intersections
            offset += 1
        #check if fits at end
        fits = True
        intersections = 0
        for i in range(0,string_len-2):
            #check for vaccancy and for collisions
            if ((string[i]!=line_str[i+offset] and line_str[i+offset]!=VOID_CHAR)
                    or line_dir_str[i+offset] == direction 
                    or line_dir_str[i+offset] == BOTH_DIR):
                fits = False
                break
            #else
            if (line_str[i+offset]!=VOID_CHAR 
                    and line_str[i+offset]!=WORD_WRAPPER_CHAR):
                intersections += 1
        if fits == True:
            if intersections > best_offset_intersections:
                best_offset = offset
                best_offset_intersections = intersections
        return best_offset,best_offset_intersections

    def add_word_to_word_list(self,string,x,y,direction):
        if string[0] == WORD_WRAPPER_CHAR:
            string = string[1:]
            if direction == HORI_DIR:
                x = x + 1
            else:
                y = y + 1
        if string[-1] == WORD_WRAPPER_CHAR:
            string = string[:-1]
        self.words.append(self.Word(string,x,y,direction))

    def apply_str_at_offset(self,position,direction,string,offset):
        string = WORD_WRAPPER_CHAR + string + WORD_WRAPPER_CHAR
        if offset == -1:
            string = string[1:]
            offset = 0
        if(direction == HORI_DIR):
            self.add_word_to_word_list(string,offset,position,direction)
            for i in range(0,len(string)):
                if (i+offset<self.__WIDTH):
                    self.__matrix[i+offset][position].set(string[i],HORI_DIR)
        else:
            self.add_word_to_word_list(string,position,offset,direction)
            for i in range(0,len(string)):
                if (i+offset<self.__HEIGHT):
                    self.__matrix[position][i+offset].set(string[i],VERT_DIR)


    def get_best_place(self,direction,string, c =False):
        best_pos = -1
        best_score = -1
        best_offset = -1
        if direction == HORI_DIR:
            dimension = self.__HEIGHT
        else:
            dimension = self.__WIDTH
        for i in range(0,dimension,2):
            if (c):
                offset, score = self.c_get_best_place_in_line(i,direction,string)
            else:
                offset, score = self.get_best_place_in_line(i,direction,string)
            if (best_score<score):
                best_score = score
                best_pos = i
                best_offset = offset
        return best_offset,best_pos,best_score

    def place_word(self,strWord, c = False):
        offset,pos,score = self.get_best_place(self.__dir_toggle,strWord, c)
        if(score==-1):
            return -1
        self.apply_str_at_offset(pos,self.__dir_toggle,strWord,offset)
        if (self.__dir_toggle == HORI_DIR):
            self.__dir_toggle = VERT_DIR
        else:
            self.__dir_toggle = HORI_DIR
        return score

    def place_word_dir(self,direction,strWord, c = False):
        offset,pos,score = self.get_best_place(direction,strWord, c)
        if(score==-1):
            return -1
        self.apply_str_at_offset(pos,direction,strWord,offset)
        return score

    def sort_dictionary_with_scores(self,dictionary, direction, c = False, kick = False):
        def getScore(str):
            offset,pos,score = self.get_best_place(direction, str, c)
            return score
        dictionary.sort(key=len, reverse = True)
        dict_and_score = [[w,getScore(w)] for w in dictionary]
        dict_and_score.sort(key = lambda x : x[1], reverse = True)
        if kick:
            dictionary = [w[0] for w in dict_and_score if w[1]>=0]
        else:
            dictionary = [w[0] for w in dict_and_score]
        return dictionary
              

    def create_crossword(self,dict_hori, dict_vert, c = False, first_time = True):
        dictionary_h = dict_hori.copy()
        dictionary_v = dict_vert.copy()
        done_vertical = False
        done_horizontal = False
        #find word with best score
        while(not done_vertical or not done_horizontal):
            if (self.__dir_toggle == HORI_DIR):
                dictionary_h = self.sort_dictionary_with_scores(dictionary_h,
                                                                HORI_DIR,
                                                                c,
                                                                kick = True)
                if dictionary_h:
                    sc = self.place_word_dir(HORI_DIR,dictionary_h[0], c)
                    removed = dictionary_h.pop(0)
                    if removed in dictionary_v: dictionary_v.remove(removed)
                else:
                    done_horizontal = True
                    sc = -1
                if not first_time and sc <= 0:
                    done_horizontal = True
                self.__dir_toggle = VERT_DIR

            # if direction is vertical
            else: 
                dictionary_v = self.sort_dictionary_with_scores(dictionary_v,
                                                                VERT_DIR,
                                                                c,
                                                                kick = True)
                if dictionary_v:
                    sc = self.place_word_dir(VERT_DIR,dictionary_v[0], c)
                    removed = dictionary_v.pop(0)
                    if removed in dictionary_h: dictionary_h.remove(removed)
                else:
                    done_vertical = True
                    sc = -1
                if not first_time and sc <= 0:
                    done_vertical = True
                self.__dir_toggle = HORI_DIR

            #end of while
            first_time = False           

    def count_intersections(self):
        intersections = 0
        for i in range(0,self.__WIDTH):
            for j in range(0,self.__HEIGHT):
                if self.__matrix[i][j].get_dir() == BOTH_DIR:
                    intersections += 1
        return intersections

    def get_intersection_ratio(self):
        intersections = 0
        no_intersection = 0
        for i in range(0,self.__WIDTH):
            for j in range(0,self.__HEIGHT):
                if self.__matrix[i][j].get_dir() == BOTH_DIR:
                    intersections += 1
                elif (self.__matrix[i][j].get_dir() == VERT_DIR 
                      or self.__matrix[i][j].get_dir() == HORI_DIR):
                    no_intersection += 1
        if (no_intersection+intersections == 0):
            return -1
        return intersections/no_intersection#(noIntersection+intersections)

