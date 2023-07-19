import unittest
import os
import sys
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(currentDir, '../src'))
from crosswordMatrix import Matrix
import crosswordMatrix
import ctypes


class testUpdateUserList(unittest.TestCase):

    def testInterface(self):
        #return     
        cfunctions = ctypes.CDLL(".\\lib\\cfunctions.so")
        string = ctypes.create_string_buffer(b"123456789")
        sizeX = ctypes.c_int(3)
        sizeY = ctypes.c_int(4)
        x = ctypes.c_int(-1)
        y = ctypes.c_int(-1)
        pyTestInterface = cfunctions.test_interface
        pyTestInterface.argtypes = [
            ctypes.c_int, 
            ctypes.c_int, 
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_char_p
            ]
        pyTestInterface.restype = ctypes.c_int

        cIntReturn = pyTestInterface(sizeX,sizeY,ctypes.byref(x),ctypes.byref(y),string)
        print("resultado: x="+str(x.value)+" y="+str(y.value))
        self.assertEqual(1,cIntReturn)
        self.assertEqual(string.value, b'abcdefghi')
        self.assertEqual(x.value,2)
        self.assertEqual(y.value,3)
    
    # TODO continuar daqui, lembrar (testar as duas funcoes,
    # em C e em Python, o resultado tem que ser o mesmo)
    def testGetBestPlace(self):
        mat = Matrix(14,14)
        word = "paalavra,".replace(" ",crosswordMatrix.VOID_CHAR).replace(",",crosswordMatrix.WORD_WRAPPER_CHAR)
        word2 = ",vertical,".replace(" ",crosswordMatrix.VOID_CHAR).replace(",",crosswordMatrix.WORD_WRAPPER_CHAR)
        word3 = "paaa".replace(" ",crosswordMatrix.VOID_CHAR).replace(",",crosswordMatrix.WORD_WRAPPER_CHAR)
        word4 = ",asdasdff,".replace(" ",crosswordMatrix.VOID_CHAR).replace(",",crosswordMatrix.WORD_WRAPPER_CHAR)
        word5 = ",pli,".replace(" ",crosswordMatrix.VOID_CHAR).replace(",",crosswordMatrix.WORD_WRAPPER_CHAR)
        word6 = ",vefghl".replace(" ",crosswordMatrix.VOID_CHAR).replace(",",crosswordMatrix.WORD_WRAPPER_CHAR)
        mat.apply_str_at_offset(4,crosswordMatrix.HORI_DIR,word,0)
        mat.apply_str_at_offset(2,crosswordMatrix.VERT_DIR,word2,2)
        mat.apply_str_at_offset(4,crosswordMatrix.HORI_DIR,word3,5)
        mat.apply_str_at_offset(6,crosswordMatrix.VERT_DIR,word4,4)
        mat.apply_str_at_offset(8,crosswordMatrix.HORI_DIR,word5,0)
        mat.apply_str_at_offset(10,crosswordMatrix.VERT_DIR,word6,7)
        ####
        print("best place: " + str(mat.get_best_place(crosswordMatrix.HORI_DIR,"taaad")))
        print("bpil: "+str(mat.get_best_place_in_line(6,crosswordMatrix.HORI_DIR,"taaad")))
        print("bpil_c: "+str(mat.c_get_best_place_in_line(6,crosswordMatrix.VERT_DIR,"taaad")))
        print(mat.get_best_place_in_line(1,crosswordMatrix.VERT_DIR,"alla"))
        print(mat.c_get_best_place_in_line(5,crosswordMatrix.HORI_DIR,"avra"))
        print(mat.c_get_best_place_in_line(5,crosswordMatrix.HORI_DIR,"avra"))
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"avra")
        mat.printM(',','.')


# Executar os testes
if __name__ == 'a__main__':
    mat = Matrix(14,14)
    # c functions must be equal python ones
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"abcabcaababaa")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"bcabcabbabb")
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"cabcabcsbs")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"abcabcabc")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"bcdefghi")
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"arfrbr")
    #mat.placeWordDir(crosswordMatrix.HORI_DIR,"bcdefghi")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"btbtttttotttx")
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"zzzzzzzzxzzzpz") 
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"zzzzzzzzxzzzpz") #shouldnt insert
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"acogwyui") #FAIL word wrapper impede palavra de chegar ate o fim
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"acaaaaaauaaapa") #FAIL word wrapper impede palavra de chegar ate o fim
    bestoOffset, score = mat.c_get_best_place_in_line(4, crosswordMatrix.HORI_DIR, "dacae")
    print("bestOffset: " + str(bestoOffset) + " score: " + str(score))
    mat2 = Matrix(14,14)
    mat2.set_char('a',0,4)
    offset, score = mat2.get_best_place_in_line(0,crosswordMatrix.HORI_DIR,"abcabcaababa")
    c_offset, c_score = mat2.c_get_best_place_in_line(0,crosswordMatrix.HORI_DIR,"abcabcaababa")
    print("offset: " + str(score) + " c_offset: " + str(score))
    print("score: " + str(score) + " c_score: " + str(score))
    #mat2.placeWordDir(crosswordMatrix.HORI_DIR,"abcabcaababaa")
    #mat2.placeWordDir(crosswordMatrix.HORI_DIR,"abcabcaababaa")
    mat2.printM()
    #unittest.main()

if __name__ == '__main__2':
    mat = Matrix(14,14)
    # c functions must be equal python ones
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"abcabcaababaa")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"bcabcabbabb")
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"cabcabcsbs")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"abcabcabc")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"bcdefghi")
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"arfrbr")
    #mat.placeWordDir(crosswordMatrix.HORI_DIR,"bcdefghi")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"btbtttttotttx")
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"zzzzzzzzxzzzpz") 
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"zzzzzzzzxzzzpz") #shouldnt insert
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"acogwyui") #FAIL word wrapper impede palavra de chegar ate o fim
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"acaaaaaauaaapa") #FAIL word wrapper impede palavra de chegar ate o fim
    mat.printM('.',' ')
    #TODO assert para mat.getBestPlace(crosswordMatrix.HORI_DIR,"daca") = (2, 4, 2)
    print("######## PYTHON #########")
    print(mat.get_best_place(crosswordMatrix.HORI_DIR,"daca"))
    #TODO assert para mat.getBestPlace(crosswordMatrix.HORI_DIR,"daca") = (2, 2)
    #TODO vertical ta horizontal e horizontal ta vertical kk
    #TODO testar com casos de palavras na mesma direcao
    print(mat.get_best_place_in_line(6,crosswordMatrix.VERT_DIR,"dacaaza"))
    print("######## C ########")
    touple = mat.c_get_best_place_in_line(6,crosswordMatrix.VERT_DIR,"dacaaza")
    print("######## AFTER C ########")
    print(touple)
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"dacaaza")
    mat.printM('.',' ')

if __name__ == '__main__':
    mat = Matrix(14,14)
    mat_c = Matrix(14,14)
    # c functions must be equal python ones
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"abcabcaababaa")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"bcabcabbabb")
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"cabcabcsbs")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"abcabcabc")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"bcdefghi")
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"arfrbr")
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"btbtttttotttx")
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"zzzzzzzzxzzzpz") 
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"zzzzzzzzxzzzpz") #shouldnt insert
    mat.place_word_dir(crosswordMatrix.HORI_DIR,"acogwyui") #FAIL word wrapper impede palavra de chegar ate o fim
    mat.place_word_dir(crosswordMatrix.VERT_DIR,"acaaaaaauaaapa")

    mat_c.place_word_dir(crosswordMatrix.HORI_DIR,"abcabcaababaa", c = True)
    mat_c.place_word_dir(crosswordMatrix.VERT_DIR,"bcabcabbabb", c = True)
    mat_c.place_word_dir(crosswordMatrix.HORI_DIR,"cabcabcsbs", c = True)
    mat_c.place_word_dir(crosswordMatrix.VERT_DIR,"abcabcabc", c = True)
    mat_c.place_word_dir(crosswordMatrix.VERT_DIR,"bcdefghi", c = True)
    mat_c.place_word_dir(crosswordMatrix.HORI_DIR,"arfrbr", c = True)
    mat_c.place_word_dir(crosswordMatrix.VERT_DIR,"btbtttttotttx", c = True)
    mat_c.place_word_dir(crosswordMatrix.HORI_DIR,"zzzzzzzzxzzzpz", c = True)
    mat_c.place_word_dir(crosswordMatrix.HORI_DIR,"zzzzzzzzxzzzpz", c = True) #shouldnt insert
    mat_c.place_word_dir(crosswordMatrix.HORI_DIR,"acogwyui", c = True) #FAIL word wrapper impede palavra de chegar ate o fim
    mat_c.place_word_dir(crosswordMatrix.VERT_DIR,"acaaaaaauaaapa", c = True)

    k = 3
