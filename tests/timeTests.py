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
import io
import cProfile
import pstats

def timeLookAheadAlg(iterations = 1):
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

def timeBruteForceAlg(iterations):
    dictionary = fileHandler.getDictionaries()
    matrix,bestRatioMatrix,scores = algorythms.bruteForce(width=14,height=14,dictionary=dictionary,iterations=iterations)
    matrix.printM()

def logPerformance():
    date = pd.to_datetime(datetime.datetime.now())
    time, score = timeLookAheadAlg(1)
    data = {
    'date': [date],
    'time': [time],
    'score': [score]
    }
    #save to file
    try:
        df = pd.read_csv("timesLog.csv")
        print("Appending to results.csv")
        df.append(data)
    except FileNotFoundError:
        df = pd.DataFrame(data)
        df.to_csv("timesLog.csv", index=False)
    
def profile(command,locals, outputName):
    prof = cProfile.Profile()
    prof.runctx(command, None, locals)
    prof.dump_stats('outputName.prof')
    stream = open(outputName + '.txt', 'w')
    stats = pstats.Stats('outputName.prof', stream=stream)
    stats.sort_stats('cumtime')
    stats.print_stats()

if __name__ == "__main__":
    #profile("timeBruteForceAlg(10)", locals = locals(), outputName="ProfileOfBruteForce")
    logPerformance()