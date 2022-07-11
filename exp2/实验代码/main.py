from IO import IO
from myope import ope

if __name__ == "__main__":
    datasetIO = IO(1000000,'NE.txt','password_table.txt')
    dataope = ope(datasetIO)
    plaintext,cipher = dataope.encrypt(354778)
    print(cipher)
    print(dataope.decrypt(cipher))