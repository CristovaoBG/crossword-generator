import random
import os
from defs import *

# WIDTH = 20
# HEIGHT = 30

def read_dictionary_files(path):
    output = []
    for fileName in os.listdir(path):
        filePath = os.path.join(path, fileName)
        if os.path.isfile(filePath):
            with open(filePath, 'r') as file:
                for line in file:
                    words = line.split()
                    if(words):
                        output.append(words[0])
    # remove duplicates
    output = list(set(output))
    return output 

def open_dictionary(filename):
    dictionary = []
    #imports dictionary and sorts
    with open(filename) as file:
        dictionary = file.read().split('\n')
    rand = lambda a : random.random()
    dictionary.sort(key = rand)
    return dictionary

def save_string(string, filename):
    os.makedirs(os.path.dirname(filename), exist_ok = True)
    with open(filename, "w") as text_file:
        n = text_file.write(string)
    return n

def read_used_words():
    current_path = os.getcwd()
    current_path += "\\data\\output"
    files_path = []
    for r, d, f in os.walk(current_path):
        for file in f:
            if 'Words' in file:
                files_path.append(os.path.join(r, file))
    #readAllWords
    used_words = []
    for f in files_path:
        with open(f) as file:
             words = file.read().split('\n')
        for word in words:
            if (word != ""):
                used_words.append(word)
    return used_words

def get_dictionaries():
    #return openDictionary(INPUT_PATH + "/" + DICTIONARY_FILE_NAME)
    return read_dictionary_files(".\\data\\input")
