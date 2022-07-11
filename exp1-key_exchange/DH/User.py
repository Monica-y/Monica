# g = 5,p = 509
# 先创建通信双方，一个User类
class User:
    my_key = 0
    send_to_other_key = 0
    AES_key = 0
    g = 5
    p = 509

    def __init__(self,my_key,p,g):
        self.my_key = my_key
        self.g = g
        self.p = p
        self.send_to_other_key = pow(self.g,my_key,self.p)

    def calculateAESKey(self,come_from_other_key):
        self.AES_key = pow(come_from_other_key,self.my_key,self.p)
        return self.AES_key
