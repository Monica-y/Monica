# 使用DH协议交换密钥，对交换的密钥使用MD5码计算得128bit，作为AES算法密钥保存在文件中
import hashlib
from msilib.schema import Class

# md5 = hashlib.md5()

class MD5:
    # 待加密信息
    str = 'null'
    filename = 'null'
    md5 = 0

    # 创建MD5对象
    def __init__(self,str):
        self.str = str
        # self.filename = filename
        self.md5 = hashlib.md5()

    def md5Encode(self):
        # 此处必须声明encode
        self.md5.update(self.str.encode('utf-8'))
        result = self.md5.hexdigest()
        key = result[0:16]
        return key
        # for index in range(16):
        #     key[index] = key[index]+result[index]
        # return key

        # print('MD5加密前为'+self.str)
        # print('The MD5 value is '+result)

        # file = open(self.filename,'w')
        # file.write(result)
        # file.close()
