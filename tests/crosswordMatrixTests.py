import unittest
import os
import sys
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(currentDir, '../src'))
from crosswordMatrix import Matrix
import crosswordMatrix


class testUpdateUserList(unittest.TestCase):

    
    def testBestPlaceInLineMiddle(self):
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
        mat = Matrix(14,14)
        #newMat.createCrossword(dictionary)
        mat.placeWordDir(crosswordMatrix.HORI_DIR,"abcabcaababaa")
        mat.placeWordDir(crosswordMatrix.VERT_DIR,"bcabcabbabb")
        mat.placeWordDir(crosswordMatrix.HORI_DIR,"cabcabcsbs")
        mat.placeWordDir(crosswordMatrix.VERT_DIR,"abcabcabc")
        mat.placeWordDir(crosswordMatrix.VERT_DIR,"bcdefghi")
        mat.placeWordDir(crosswordMatrix.HORI_DIR,"arfrbr")
        #mat.placeWordDir(crosswordMatrix.HORI_DIR,"bcdefghi")
        mat.placeWordDir(crosswordMatrix.VERT_DIR,"btbtttttotttx")
        mat.placeWordDir(crosswordMatrix.HORI_DIR,"zzzzzzzzxzzzpz") 
        mat.placeWordDir(crosswordMatrix.HORI_DIR,"zzzzzzzzxzzzpz") #shouldnt insert
        mat.placeWordDir(crosswordMatrix.HORI_DIR,"acogwyui") #FAIL word wrapper impede palavra de chegar ate o fim
        mat.placeWordDir(crosswordMatrix.VERT_DIR,"acaaaaaauaaapa") #FAIL word wrapper impede palavra de chegar ate o fim
        # import pyperclip
        # pyperclip.copy(mat.getMatrixString())
        self.assertEqual(assertMatString,mat.getMatrixString())
        

# Executar os testes
# TODO make it work on VSCODE (only works in powershell)
if __name__ == '__main__':
    unittest.main()