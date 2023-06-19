import os
import sys
import time
import datetime
import pandas as pd
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(currentDir, '../src'))
import fileHandler
import crosswordMatrix
import algorythms

def timeLookAheadAlg(iterations):
    score = 0
    start_time = time.time()
    dictionary = fileHandler.getDictionaries()
    matrix = crosswordMatrix.Matrix(width=14,height=14)
    for i in range(iterations):
        matrix, usedWords = algorythms.lookAhead(width=14,height=14,dictionaryOrig=dictionary,lookOverXTopWords=3)
        score+=matrix.countIntersections()
        for word in usedWords:
            dictionary.pop(dictionary.index(word))
    score/=iterations
    return time.time()-start_time, score
# readUsedWords()

if __name__ == "__main__":
    date = pd.to_datetime(datetime.datetime.now())
    time, score = timeLookAheadAlg(10)
    data = {
    'date': [date],
    'time': [time],
    'score': [score]
    }
    #save to file
    try:
        df = pd.read_csv("results.csv")
        print("Appending to results.csv")
        df.append(data)
    except FileNotFoundError:
        df = pd.DataFrame(data)
        df.to_csv("results.csv", index=False)
    
