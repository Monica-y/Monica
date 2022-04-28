# imports
import decimal  # to handle very big numbers
from math import gcd
# 费马小定理：对于质数p和任意整数a，有a^p ≡ a(mod p)(同余)。反之，若满足a^p ≡ a(mod p)，p也有很大概率为质数。
# 将两边同时约去一个a，则有a^(p-1) ≡ 1(mod p)
# 如果p是奇素数，则 x^2 ≡ 1(mod p)的解为 x ≡ 1 或 x ≡ p - 1(mod p)(二次探测定理)
# 假设n=341，我们选取的a=2。则第一次测试时，2^340 mod 341=1。由于340是偶数，因此我们检查2^170，得到2^170 mod 341=1，
# 满足二次探测定理。同时由于170还是偶数，因此我们进一步检查2^85 mod 341=32。此时不满足二次探测定理，因此可以判定341不为质数。
# 我的算法直接找到最小的指数开始尝试，判断的依据是二次探测定理
class PrimeD:
    def __init__(self) -> None:
        pass
    def PrimeDetection(self,aim)->bool:
        # initial values
        # n = 1056048717
        n = aim
        m = 0
        # limit num of calculations, gives the precision
        limit = 200000

        # find m from the equation:  n-1 = 2^k*m
        k = 0
        # run until result of division is not an integer
        # when n is oushu ，find the min(m)
        result = 0
        while result == 0:
            result = (n-1) % (2**k)
            if result == 0:
                m = (n-1)//(2**k)
                # 整数除法，返回商的整数部分（向下取整）
                k += 1

        # pick an a in the range of: 1 < a < n-1
        a = 2

        # Calculate the cases of primarity
        # for b0: b0 = a^m mod n
        b = (a**m) % n
        count = 1 # 记录探定的次数
        print(aim)
        if(abs(b) == 1):  # probably prime if b is -1 or +1
            print(" is PROBABLY prime!")
            return True
        else:
            # for b1 to bn, stops when b == 1 or b == n-1 or limit encountered
            # b==-1 in mod is the same as b == n-1
            # from a^m to a^(n-1)
            while b != 1 and b != (n-1) and count != limit:
                b = (b**2) % n
                count += 1
            # get final results of primarity testing for b to bn
            if(b == n-1):
                print(" is PROBABLY prime!")
                return True
            if(b == 1 or count == limit):
                print(" is composite")
                return False

    def primitiveRoots(self,primeNum):
        if primeNum >5:
            if pow(5,primeNum-1,primeNum)==1:
                return 5
        else:
            if pow(2,primeNum-1,primeNum)==1:
                return 2
        # 如果2和5都不是原根，那就随机选择原根list中的第十个元素为g
        possible_set = {num for num in range(1, primeNum) if gcd(num, primeNum) }
        root_list = [base for base in range(1, primeNum) if possible_set == {pow(base, power, primeNum) for power in range(1, primeNum)}]
        return root_list[10]