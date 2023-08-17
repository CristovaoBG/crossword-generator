import fileHandler
import algorythms
import crosswordMatrix
from defs import *
import copy
import os

def generate_crosswords_and_files(width, height, n_of_crosswords_to_generate, minimum_score, dictionary, c = False):
    used_words = fileHandler.read_used_words()
    dictionary = [d for d in dictionary if d not in used_words]
    # dictionary = dictionary[0:100] ##########DEBUG
    for i in range(0,n_of_crosswords_to_generate):
        matrix = crosswordMatrix.Matrix(width,height)
        while (matrix.count_intersections()<minimum_score):
            matrix, used_words = algorythms.look_ahead(width,height,dictionary,5, c)#LOOK_OVER_X_TOP_WORDS)
        matrix.printM(" "," ")
        used_words_str = ""
        for word in used_words:
            used_words_str += word + '\n'
            dictionary.pop(dictionary.index(word))
        #create files
        matrixString = matrix.get_matrix_string()
        offset = 0
        while(os.path.isfile(OUTPUT_PATH+"\crossword"+str(offset+i)+"\Descriptor.txt")):
            offset += 1

        fileHandler.save_string(matrix.get_matrix_string(),
                               f"{OUTPUT_PATH}\crossword{i+offset}\Layout.txt")
        fileHandler.save_string(matrix.get_directions_string(),
                               f"{OUTPUT_PATH}\crossword{i+offset}\Directions.txt")
        fileHandler.save_string(matrix.get_matrix_descriptor_str(),
                               f"{OUTPUT_PATH}\crossword{i+offset}\Descriptor.txt")
        fileHandler.save_string(used_words_str,
                               f"{OUTPUT_PATH}\crossword{i+offset}\Words.txt")


def find_forever(width, height, n_of_crosswords_to_generate, minimum_score, dictionary, c = False):
    
    used_words = fileHandler.read_used_words()
    for uw in used_words:
        dictionary.pop(dictionary.index(uw))
    for i in range(0,n_of_crosswords_to_generate):
        matrix = crosswordMatrix.Matrix(width,height)
        best_matrix = matrix
        history = []
        history_mat = []
        while (True):
            matrix, used_words = algorythms.look_ahead(width,height,dictionary,37, c)#LOOK_OVER_X_TOP_WORDS)
            history.append(matrix.count_intersections())
            history_mat.append(copy.deepcopy(matrix))
            if matrix.count_intersections() > best_matrix.count_intersections():
                best_matrix = matrix

if __name__=="__main__":
    dictionary = fileHandler.get_dictionaries()

    generate_crosswords_and_files(width=WIDTH, height=HEIGHT, n_of_crosswords_to_generate=15, minimum_score=35, dictionary=dictionary, c = True)
