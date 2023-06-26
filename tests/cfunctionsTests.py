import unittest
import os
import sys
currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(currentDir, '../src'))
from crosswordMatrix import Matrix
import crosswordMatrix
import ctypes


class testUpdateUserList(unittest.TestCase):

    def simpleTest(self):
        cfunctions = ctypes.CDLL("H:\\Cris\\programacao\\crosswordGen\\crosswordGenerator\\lib\\cfunctions.so")
        cfunctions.test()

    def testInterface(self):
        return     
        cfunctions = ctypes.CDLL("H:\\Cris\\programacao\\crosswordGen\\crosswordGenerator\\lib\\cfunctions.so")
        string = ctypes.create_string_buffer(b"123456789") #3x3 matrix
        sizeX = ctypes.c_int(3)
        sizeY = ctypes.c_int(3)
        x = ctypes.c_int(-1)
        y = ctypes.c_int(-1)
        pyTestInterface = cfunctions.testInterface
        pyTestInterface.argtypes = [
            ctypes.c_int, 
            ctypes.c_int, 
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_char_p
            ]
        pyTestInterface.restype = None

        pyTestInterface(sizeX,sizeY,ctypes.byref(x),ctypes.byref(y),string)

        print(string.value)
        #self.assertEqual()
        

# Executar os testes
if __name__ == '__main__':
    cfunctions = ctypes.CDLL("H:/Cris/programacao/crosswordGen/crosswordGenerator/lib/cfunctions.so")
    cfunctions.test()
    unittest.main()