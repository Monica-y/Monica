from position import position
from IO import IO
import random
import numpy as np

class ope:
    plaintext_area = []
    ciphertext_area = []
    # 密码表路径(写读) 密文-明文
    datasetIO = IO(1000000,'','')
    _no_value = object()

    def __init__(self,datasetIO) -> None:
        for i in range(999999):
            self.plaintext_area.append(i+1)
        for i in range(9999999):
            self.ciphertext_area.append(i+1)
        self.datasetIO = datasetIO

        # 超几何分布采样函数
    def HGD(self,plaintext_area,ciphertext_area):
        # 明文域的长度
        len_plaintext = len(plaintext_area)
        # 密文域的长度
        len_ciphertext =len(ciphertext_area)
        # 模拟在密文域中抽一半数量的球
        y = int(len_plaintext/2)
        x = np.random.hypergeometric(len_plaintext,len_ciphertext,y,size=1)
        # size规定了返回结果的大小，这里是一元组。
        # 该函数表示对一个超几何分布进行采样，ngood表示成功标志元素个数，nbad表示没有成功标志元素个数，nsample表示抽样次数，函数返回抽取nsample个元素中具有成功标志的元素个数。
        plaintext_index = x[0]
        if x[0]>= len_plaintext:
            plaintext_index = len_plaintext-1
        return plaintext_area[plaintext_index]

    def encrypt(self,plaintext,plaintext_area =_no_value,ciphertext_area = _no_value):
        if plaintext_area == self._no_value:
            plaintext_area = self.plaintext_area
        if ciphertext_area == self._no_value:
            ciphertext_area = self.ciphertext_area
        # 计算明文域的大小
        plaintext_field = max(plaintext_area)-min(plaintext_area)+1
        # 计算密文域的大小
        ciphertext_field = max(ciphertext_area)-min(ciphertext_area)+1
        # 计算密文的中心
        ciphertext_center = int((max(ciphertext_area)+min(ciphertext_area))/2)
        ma = max(ciphertext_area)
        mi = min(ciphertext_area)
        plaintext_center = self.datasetIO.searchPassword(ciphertext_center)
        if plaintext_center == -1:
            plaintext_center = self.HGD(plaintext_area,ciphertext_area)
            data = []
            pos = position(ciphertext_center,plaintext_center)
            data.append(pos)
            self.datasetIO.writePassword(data)

        if plaintext_field == 1:
            #此时明文中只含有一个值，那么我们只需要在密文域中任意寻找一个值作为密文
            cipher = random.randint(min(ciphertext_area),max(ciphertext_area))
            data = []
            pos = position(cipher,plaintext)
            data.append(pos)
            self.datasetIO.writePassword(data)
            return plaintext,cipher

        if plaintext_field == 2:
            # 此时明文中只含有两个值，我们传入的plaintext可能是明文域的左端点，也可能是明文域的右端点
            if min(plaintext_area) == plaintext:
                # 明文为明文域的左端点，所以密文区间是密文域的左半边
                cipher = random.randint(min(ciphertext_area),ciphertext_center)
                data = []
                pos = position(cipher,plaintext)
                data.append(pos)
                self.datasetIO.writePassword(data)
                return plaintext,cipher
            else:
                # 明文为明文域的右端点，所以密文区间是密文域的右半边
                cipher = random.randint(ciphertext_center+1,max(ciphertext_area))
                data = []
                pos = position(cipher,plaintext)
                data.append(pos)
                self.datasetIO.writePassword(data)
                return plaintext,cipher

        if plaintext<=plaintext_center:
            # 下一步应该向密文域左半边搜索，同时明文域范围缩减到左半边
            newPlaintext_area = []
            for i in range(min(plaintext_area),plaintext_center+1):
                newPlaintext_area.append(i)
            newCiphertext_area = []
            for i in range(min(ciphertext_area),ciphertext_center+1):
                newCiphertext_area.append(i)
        else:
            # 下一步应该向密文域右半边搜索，同时明文域范围缩减到右半边
            newPlaintext_area = []
            for i in range(plaintext_center+1,max(plaintext_area)+1):
                newPlaintext_area.append(i)
            newCiphertext_area = []
            temp = max(ciphertext_area)+1
            for i in range(ciphertext_center+1,max(ciphertext_area)+1):
                newCiphertext_area.append(i)
        return self.encrypt(plaintext,newPlaintext_area,newCiphertext_area)

    def decrypt(self,ciphertext,plaintext_area = _no_value,ciphertext_area = _no_value):
        if plaintext_area == self._no_value:
            plaintext_area = self.plaintext_area
        if ciphertext_area == self._no_value:
            ciphertext_area = self.ciphertext_area        
        plaintext_field = max(plaintext_area)-min(plaintext_area)
        ciphertext_field = max(ciphertext_area)-min(ciphertext_area)
        # 计算密文中心
        ciphertext_center = int((max(ciphertext_area)+min(ciphertext_area))/2)

        if plaintext_field == 1:
            # 此时明文域中只有一个明文，就一定是该密文对应的明文
            return min(plaintext_area)
        if plaintext_field == 2:
            if ciphertext<=ciphertext_center:
                # 此时密文对应的明文是明文域的左端点
                return min(plaintext_area)
            else:
                # 此时密文对应的明文是明文域的右端点
                return max(plaintext_area)
        plaintext_center = self.datasetIO.searchPassword(ciphertext_center)
        # 这里不做异常处理，我们假设需要解密的密文一定能从密码表中查找出来

        if ciphertext<=ciphertext_center:
            # 下一步应该向密文域左半边搜索，同时明文域范围缩减到左半边
            newPlaintext_area = []
            for i in range(min(plaintext_area),plaintext_center+1):
                newPlaintext_area.append(i)
            newCiphertext_area = []
            for i in range(min(ciphertext_area),ciphertext_center+1):
                newCiphertext_area.append(i)
        else:
            newPlaintext_area = []
            for i in range(plaintext_center+1,max(plaintext_area)+1):
                newPlaintext_area.append(i)
            newCiphertext_area = []
            for i in range(ciphertext_center+1,max(ciphertext_area)+1):
                newCiphertext_area.append(i)
        return self.decrypt(ciphertext,newPlaintext_area,newCiphertext_area)