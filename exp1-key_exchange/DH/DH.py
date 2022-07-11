import random
from DH.User import User
from DH.MD5 import MD5
from DH.PrimeDetection  import PrimeD

def find_pg():
    # 生成p，使用Miller Rabin算法进行素性检测
    print("#########################################################")
    print("Generate a random number and check if it is prime:")
    p = random.randint(1,999999999)
    primeDetect = PrimeD()
    while(not primeDetect.PrimeDetection(p)):
        p = random.randint(1,999999999)
    print("The final chosen prime number is "+str(p))
    # 根据p计算g,g一般不会很大，选择2或5,失败则返回-1
    print("#########################################################")
    print("Determine g from p:")
    g = primeDetect.primitiveRoots(p)
    print("The final chosen g is "+str(g))
    return p,g

def DH(p,g)->User: 

    # 模拟Alice和Bob生成各自的密钥
    print("#########################################################")
    print("User generate their own keys:")
    Alice = User(random.randint(1,999),p,g)
    print("User's key is "+ str(Alice.my_key))
    return Alice
    # 模拟交换密钥的过程
    # print("#########################################################")
    # print("Step 4 Simulate the process of Bob and Alice exchanging keys:")
    # Alice_key = str(Alice.calculateAESKey(Bob.send_to_other_key))
    # Bob_key = str(Bob.calculateAESKey(Alice.send_to_other_key))
    # print("Alice gets the key "+ Alice_key)
    # print("Bob gets the key "+ Bob_key)
    # # 对得到的密钥计算MD5值，得到AES需要的128bit密钥，并输出密钥值
    # print("#########################################################")
    # print("Step 5 The final key is obtained by calculating MD5")
    # Alice_MD5 = MD5(Alice_key,"Alice_MD5.txt")
    # BoB_MD5 = MD5(Bob_key,"BoB_MD5.txt")
    # Alice_MD5.md5Encode()
    # BoB_MD5.md5Encode()
    # print("#########################################################")
    # print("The key exchange is complete. The key is already stored in the local file")
