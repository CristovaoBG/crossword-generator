import unittest
import os
import sys
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(currentDir, '../src'))
from crosswordMatrix import Matrix
import crosswordMatrix


class testUpdateUserList(unittest.TestCase):
    assertMatString = """   abcabcaababaa.
                            b'.'c'''t'''c'
                            cabcabcsbs.'a'
                            a'c'b'''t'''a'
                            b'd'c'''t'''a'
                            c'e'a'''t'''a'
                            arfrbr.'t'''a'
                            b'g'b'''t'''a'
                            c'h'a.acogwyui
                            .'i'b'''t'''a'
                            ''.'b'''t'''a'
                            ''''.'''t'''a'
                            zzzzzzzzxzzzpz
                            ''''''''.'''a'
                            """.replace('\t','').replace(' ','')

    def testPlaceWordDir(self):
        mat = Matrix(14,14)
        #newMat.createCrossword(dictionary)
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"abcabcaababaa")#
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"bcabcabbabb")
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"cabcabcsbs")#
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"abcabcabc")
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"bcdefghi")
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"arfrbr")#
        #mat.placeWordDir(crosswordMatrix.HORI_DIR,"bcdefghi")
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"btbtttttotttx")
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"zzzzzzzzxzzzpz") #
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"zzzzzzzzxzzzpz") # #shouldnt insert
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"acogwyui") # #FAIL word wrapper impede palavra de chegar ate o fim
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"acaaaaaauaaapa") #FAIL word wrapper impede palavra de chegar ate o fim
        # import pyperclip
        # pyperclip.copy(mat.getMatrixString())
        self.assertEqual(self.assertMatString,mat.get_matrix_string())

    def testPlaceWordDir_c(self):
        mat = Matrix(14,14)
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"abcabcaababaa", True)#
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"bcabcabbabb", True)
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"cabcabcsbs", True)#
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"abcabcabc", True)
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"bcdefghi", True)
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"arfrbr", True)#
        #mat.placeWordDir(crosswordMatrix.HORI_DIR,"bcdefghi")
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"btbtttttotttx", True)
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"zzzzzzzzxzzzpz", True) #
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"zzzzzzzzxzzzpz", True) # #shouldnt insert
        mat.place_word_dir(crosswordMatrix.VERT_DIR,"acogwyui", True) # #FAIL word wrapper impede palavra de chegar ate o fim
        mat.place_word_dir(crosswordMatrix.HORI_DIR,"acaaaaaauaaapa", True) #FAIL word wrapper impede palavra de chegar ate o fim
        self.assertEqual(self.assertMatString,mat.get_matrix_string())
        
    def testBlockedIfTooBig(self):
        mat = Matrix(14,14)        
        bp = mat.get_best_place(crosswordMatrix.VERT_DIR,"aaaaaaaaaaaaaa")
        self.assertEqual((-1, 0, 0),bp)
        bp = mat.get_best_place(crosswordMatrix.VERT_DIR,"aaaaaaaaaaaaaaa")
        self.assertEqual((-1, -1, -1),bp)
        bp = mat.get_best_place(crosswordMatrix.HORI_DIR,"aaaaaaaaaaaaaa")
        self.assertEqual((-1, 0, 0),bp)
        bp = mat.get_best_place(crosswordMatrix.HORI_DIR,"aaaaaaaaaaaaaaa")
        self.assertEqual((-1, -1, -1),bp)

    def testBlockedIfTooBig_c(self):
        mat = Matrix(14,14)        
        bp = mat.get_best_place(crosswordMatrix.VERT_DIR,"aaaaaaaaaaaaaa", True)
        self.assertEqual((-1, 0, 0),bp)
        bp = mat.get_best_place(crosswordMatrix.VERT_DIR,"aaaaaaaaaaaaaaa", True)
        self.assertEqual((-1, -1, -1),bp)
        bp = mat.get_best_place(crosswordMatrix.HORI_DIR,"aaaaaaaaaaaaaa", True)
        self.assertEqual((-1, 0, 0),bp)
        bp = mat.get_best_place(crosswordMatrix.HORI_DIR,"aaaaaaaaaaaaaaa", True)
        self.assertEqual((-1, -1, -1),bp)


# Executar os testes
if __name__ == '__main__':
    unittest.main()