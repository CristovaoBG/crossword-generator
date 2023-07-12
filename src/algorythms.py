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

    def calculatesFutureScore(dictionaryH, dictionaryV, word, matrix):
        newMatrix = copy.deepcopy(matrix)
        newMatrix.placeWord(word, c)
        newDictionaryH = dictionaryH.copy()
        newDictionaryV = dictionaryV.copy()
        #remove current word of new dictionary
        if word in newDictionaryH: newDictionaryH.remove(word)
        if word in newDictionaryV: newDictionaryV.remove(word)
        newMatrix.sortDictionaryWithScores(newDictionaryH, crosswordMatrix.HORI_DIR, c)
        newMatrix.sortDictionaryWithScores(newDictionaryV, crosswordMatrix.VERT_DIR, c)
        newMatrix.createCrossword(newDictionaryH, newDictionaryV, c, firstTime = False)
        # score = newMatrix.getIntersectionRatio()
        score = newMatrix.countIntersections()
        return score, newMatrix

    dictionary = dictionaryOrig.copy()
    #if __debug__: dictionary = [w for w in dictionary if len(w)>2]
    print("dictionary size:",len(dictionary))
    matrix = crosswordMatrix.Matrix(width,height)
    usedWords = []
    #otimizavel (proprimeira palavra testada varias vezes)
    dictionaryH = dictionary.copy()
    dictionaryV = dictionary.copy()
    while True:
        print("looking for next word...")
        dictionaryH = matrix.sortDictionaryWithScores(dictionaryH, crosswordMatrix.HORI_DIR, c)
        dictionaryV = matrix.sortDictionaryWithScores(dictionaryV, crosswordMatrix.VERT_DIR, c)
        bestFutureMatrix = matrix
        
        d = dictionaryH if matrix.getCurrentDir() == crosswordMatrix.HORI_DIR else dictionaryV
        bestWord = d[0]
        bestScore = -1
        score,futureMatrix = calculatesFutureScore(dictionaryH, dictionaryV, d[0], matrix)
        if ((len(d[0]) == 3 and score==2)) or (len(d[0]) == 2 and score==1):
            bestScore = score
            bestWord = d[0]
            #bestFutureMatrix = copy.deepcopy(futureMatrix)
        else:
            for word in d[0:lookOverXTopWords if len(d) > lookOverXTopWords else len(d)]:
                # calcula o melhor score futuro das cinco melhores palavras atuais
                score,futureMatrix = calculatesFutureScore(dictionaryH, dictionaryV, word, matrix)
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
        if bestWord in dictionaryH: dictionaryH.remove(bestWord)
        if bestWord in dictionaryV: dictionaryV.remove(bestWord)
        if __debug__: futureMatrix.printM(' ',' ')
    return futureMatrix, usedWords
