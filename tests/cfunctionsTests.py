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
        #return     
        cfunctions = ctypes.CDLL("H:\\Cris\\programacao\\crosswordGen\\crosswordGenerator\\lib\\cfunctions.so")
        string = ctypes.create_string_buffer(b"123456789") #3x3 matrix
        sizeX = ctypes.c_int64(3)
        sizeY = ctypes.c_int64(4)
        x = ctypes.c_int64(-1)
        y = ctypes.c_int64(-1)
        pyTestInterface = cfunctions.testInterface
        pyTestInterface.argtypes = [
            ctypes.c_int64, 
            ctypes.c_int64, 
            ctypes.POINTER(ctypes.c_int64),
            ctypes.POINTER(ctypes.c_int64),
            ctypes.c_char_p
            ]
        pyTestInterface.restype = ctypes.c_int64

        cIntReturn = pyTestInterface(sizeX,sizeY,ctypes.byref(x),ctypes.byref(y),string)
        print("resultado: x="+str(x.value)+" y="+str(y.value))
        self.assertEqual(1,cIntReturn)
        self.assertEqual(string.value, b'abcdefghi')

        

# Executar os testes
if __name__ == '__main__':
    cfunctions = ctypes.CDLL("H:/Cris/programacao/crosswordGen/crosswordGenerator/lib/cfunctions.so")
    cfunctions.test()
    unittest.main()