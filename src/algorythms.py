import copy
import random
import crosswordMatrix


def brute_force(width,height,dictionary,iterations):
    most_intersections = -1
    best_ratio = -1
    empty_matrix = crosswordMatrix.Matrix(width,height)
    best_matrix = empty_matrix
    best_ratio_matrix = empty_matrix
    #brute forces matrix with most intersections and best ratio.
    scores = []
    for i in range(0,iterations):
        random.shuffle(dictionary)
        new_mat = crosswordMatrix.Matrix(width,height)
        new_mat.create_crossword(dictionary)
        tot_intersections = new_mat.count_intersections()
        ratio = new_mat.get_intersection_ratio()
        scores.append(ratio)
        #print("iteration:",i,"total of intersections:",tot_intersections,"intersection to letter ratio:",ratio)
        print(f"iteration: {i}, intersections: {tot_intersections}, intersection to letter ratio: {ratio}")
        if (most_intersections < tot_intersections):
            best_matrix = copy.deepcopy(new_mat)
            most_intersections = tot_intersections
        if (best_ratio < ratio):
            best_ratio_matrix = copy.deepcopy(new_mat)
            best_ratio = ratio
    return best_matrix,best_ratio_matrix,scores

def look_ahead(width, height, dictionaryOrig, look_over_x_top_words, c=False):
    """ Try the top X scoring words (look_over_x_top_words) and seeing 
    how the crossword would turn out for each one, and selecting the 
    word with highest score (most intersections). Does that for each
    word until the crossword is complete. """

    def calculates_future_score(dictionary_h, dictionary_v, word, matrix):
        new_matrix = copy.deepcopy(matrix)
        new_matrix.place_word(word, c)
        new_dictionary_h = dictionary_h.copy()
        new_dictionary_v = dictionary_v.copy()
        #remove current word of new dictionary
        if word in new_dictionary_h: new_dictionary_h.remove(word)
        if word in new_dictionary_v: new_dictionary_v.remove(word)
        new_matrix.sort_dictionary_with_scores(new_dictionary_h,
                                           crosswordMatrix.HORI_DIR, c)
        new_matrix.sort_dictionary_with_scores(new_dictionary_v,
                                           crosswordMatrix.VERT_DIR, c)
        new_matrix.create_crossword(new_dictionary_h, new_dictionary_v,
                                  c, first_time = False)
        score = new_matrix.count_intersections()
        return score, new_matrix

    dictionary = dictionaryOrig.copy()
    print("dictionary size:",len(dictionary))
    matrix = crosswordMatrix.Matrix(width,height)
    used_words = []
    # otimizavel (proprimeira palavra testada varias vezes)
    dictionary_h = dictionary.copy()
    dictionary_v = dictionary.copy()
    while True:
        print("looking for next word...")
        dictionary_h = matrix.sort_dictionary_with_scores(dictionary_h,
                                                      crosswordMatrix.HORI_DIR,
                                                      c)
        dictionary_v = matrix.sort_dictionary_with_scores(dictionary_v,
                                                      crosswordMatrix.VERT_DIR,
                                                      c)
        best_future_matrix = matrix
        
        direction = matrix.get_current_dir()
        d = dictionary_h if direction == crosswordMatrix.HORI_DIR else dictionary_v
        best_word = d[0]
        best_score = -1
        score,future_matrix = calculates_future_score(dictionary_h, dictionary_v, d[0], matrix)
        if ((len(d[0]) == 3 and score==2)) or (len(d[0]) == 2 and score==1):
            best_score = score
            best_word = d[0]
            best_future_matrix = copy.deepcopy(future_matrix)
        else:
            for word in d[0:look_over_x_top_words if len(d) > look_over_x_top_words else len(d)]:
                # calcula o melhor score futuro das cinco melhores palavras atuais
                score,future_matrix = calculates_future_score(dictionary_h,
                                                           dictionary_v,
                                                           word,
                                                           matrix)
                print(score,"-> score of",word)

                if score > best_score:
                    best_score = score
                    best_word = word
                    best_future_matrix = copy.deepcopy(future_matrix)
                # adds a little bit of impredictibility
                elif score == best_score and random.random() >= 0.5:
                    best_score = score
                    best_word = word
                    best_future_matrix = copy.deepcopy(future_matrix)

        if best_score < 0:
            break
        sc = matrix.place_word(best_word, c)
        if sc == -1:
            break
        print("selected word:",best_word,". future score:",best_score)
        used_words.append(best_word)
        # remove current word out of the dictionary
        if best_word in dictionary_h: dictionary_h.remove(best_word)
        if best_word in dictionary_v: dictionary_v.remove(best_word)
        if __debug__: best_future_matrix.printM(' ',' ')
    return future_matrix, used_words
