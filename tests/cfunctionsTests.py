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
    

# Executar os testes
if __name__ == '__main__':
    mat = Matrix(14,14)
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
    bestoOffset, score = mat.c_getBestPlaceInLine(0, 'h', "mamaco")
    unittest.main()