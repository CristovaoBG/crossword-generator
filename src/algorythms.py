import copy
import random
import crosswordMatrix


def bruteForce(width,height,dictionary,iterations):
    mostIntersections = -1
    bestRatio = -1
    emptyMatrix = crosswordMatrix.Matrix(width,height)
    bestMatrix = emptyMatrix
    bestRatioMatrix = emptyMatrix
    #brute forces matrix with most intersections and best ratio.
    scores = []
    for i in range(0,iterations):
        random.shuffle(dictionary)
        newMat = crosswordMatrix.Matrix(width,height)
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

def lookAhead(width,height,dictionaryOrig,lookOverXTopWords, c = False):

    def calculatesFutureScore(dictionary, word, matrix):
        newMatrix = copy.deepcopy(matrix)
        newMatrix.placeWord(word, c)
        newDictionary = dictionary.copy()
        #remove current word of new dictionary
        newDictionary.pop(newDictionary.index(word))
        newMatrix.sortDictionaryWithScores(newDictionary, c)
        newMatrix.createCrossword(newDictionary, c)
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
        dictionary = matrix.sortDictionaryWithScores(dictionary, c)
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
        sc = matrix.placeWord(bestWord, c)
        if sc == -1:
            break
        print("selected word:",bestWord,". future score:",bestScore)
        usedWords.append(bestWord)
        #remove current word out of the dictionary
        dictionary.pop(dictionary.index(bestWord))
    return matrix, usedWords
