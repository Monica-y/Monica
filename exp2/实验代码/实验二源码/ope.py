import csv
import random
import numpy as np 
# import pymysql

# encrypt_x = r'F:/大数据安全/第二次实验/实验代码/encrypt_x.txt'
key_table = r'F:/大数据安全/第二次实验/实验代码/实验二源码/ope.csv'
key_table1=r'F:/大数据安全/第二次实验/实验代码/实验二源码/result.csv'
inputdata = r'F:/大数据安全/第二次实验/实验代码/实验二源码/ope.txt'
def HGD(D, R):  #超几何分布进行采样
    len_D = len(D)# 明文域的长度
    len_R = len(R)# 密文域的长度
    y = int(len_R / 2) #程序模拟在密文域中抽一半数量的求
    x = np.random.hypergeometric(len_D, len_R, y, size=1)
    # size规定了返回结果的大小，这里是一元组。
    # 该函数表示对一个超几何分布进行采样，ngood表示成功标志元素个数，nbad表示没有成功标志元素个数，nsample表示抽样次数，函数返回抽取nsample个元素中具有成功标志的元素个数。
    a = x[0]
    if x[0] >= len_D:
        a = len_D - 1
    return D[a] # 返回对应明文
#写入csv文件
def writeCsv(path, data, mode): #传入变量csv文件的路径和要写入的数据
    with open(path,mode,newline="") as f: 
        writer_csv=csv.writer(f) 
        writer_csv.writerow(data) #写入相应的抽样点
        # 将row参数写入writer的文件对象，根据当前Dialect格式化。返回调用底层文件对象的write方法的返回值。

#读取csv文件
def readCsv(path): #传入变量csv文件的路径
    list_one=[]   
    with open(path,"r") as f: 
        read_scv=csv.reader(f) 
        for i in read_scv:
            list_one.append(i) #将读取到的数据追加到list列表里面
    return list_one 


def key_tableIsContain(param): #读取csv，查询是否有中心值所对应的随机数。看是否可以在密钥表中找到抽样点
    list_one = readCsv(key_table)
    # print(len(list_one))
    try:
        read = list_one[0][0]
    except BaseException:
        return 0,0
    flag = 0
    for i in range(len(list_one)):
        if str(int(param)) == list_one[i][0]:
            # 第一列是密文
            flag = 1
            return 1, int(list_one[i][1])
    if flag != 1:
        return 0, 0



def Enc2(key_table, D, R, m):
    _D = D
    _R = R
    M = max(D) - min(D) + 1
    N = max(R) - min(R) + 1
    # 计算密文的中心
    center = int((max(R) + min(R)) / 2)
    iscontain, values = key_tableIsContain(center)
    if iscontain == 1:
        c = values #记录D中的抽样值
        x = values
    else:
        # 如果密文不在密钥表(密-明对照表)中，则进行一次超几何分布采样，返回中心值对应的明文
        x = HGD(D, R)
        a = []
        a.append(center)
        a.append(x)
        writeCsv(key_table, a ,"a")#中心值和明文为一组抽样点，存进key_table中作为查询
        # “a”：此字符串用于向现有文件添加（附加）内容。如果不存在这样的文件，它会为您创建一个。
   
    if M == 1:#此时明文中只含有一个值，那么我们只需要在密文域中任意寻找一个值作为密文
        print(m)
        print("密文区间是R[%d, %d]" % (min(_R), max(_R)))
        a=random.randint(min(_R), max(_R))#在密文域随机取一个数作为m的密文
        b=[]
        b.append(a)
        b.append(m)
        writeCsv(key_table, b ,"a")#将获得的明文密文对写入key_table
        writeCsv(key_table1, b,"a")#将明文密文对写入key_table1
        return m,a
        

    if M == 2:#左端点或右端点为待求点
        print(m)
        if min(D) == m:#明文左端点为待求点
            print("密文区间是R(%d, %d]" % (min(_R), center))
            # 密文区间是密文域左半边
            a=random.randint(min(_R), center)
            b=[]
            b.append(a)
            b.append(m)
            writeCsv(key_table, b ,"a")
            writeCsv(key_table1, b,"a")
            return m,a
          
        else:#待求点是右端点
            print("密文区间是R(%d, %d]\n" % (center+1, max(_R)))
            # 密文区间是密文域右半边
            a=random.randint(center+1, max(_R))
            b=[]
            b.append(a)
            b.append(m)
            writeCsv(key_table, b ,"a")
            writeCsv(key_table1, b,"a")
            return m,a
     
    if m <= x: #左边 x是当前密文域中值对应的明文
        D = []
        for i in range(min(_D), x + 1):
            D.append(i)
        R = []
        for j in range(min(_R), center + 1):
            R.append(j)
    else:  #右边
        D = []
        for i in range(x + 1, max(_D) + 1):
            D.append(i)
        R = []
        for j in range(center + 1, max(_R) + 1):
            R.append(j)
    print("D[%d, %d] 抽样值:%d"%(min(_D), max(_D), x))
    print("R[%d, %d] 中间值:%d \n" % (min(_R), max(_R), center))
    return Enc2(key_table, D, R, m) #再次迭代

def Dnc2(key_table, D, R, m):
    # 此时m为密文
    _D = D
    _R = R
    M = max(D) - min(D) + 1
    N = max(R) - min(R) + 1
    # center是密文的中心
    center = int((max(R) + min(R)) / 2)
   
    if M == 1:
         return min(D)#最大值与最小值相等，均为明文
    if M == 2:
        if m <= center: #此时左端点为明文
             return min(D)
        else:  # m>center,右端点为明文
             return max(D)
    iscontain, values = key_tableIsContain(center)
    if iscontain == 1:
        c = values  
        x = values
    else:
        print("可能解密错误！")
        return
       

    if m <= center:  # 密文值在中心值左边
        D = []
        for i in range(min(_D), x + 1):
            D.append(i)
        R = []
        for j in range(min(_R), center + 1):
            R.append(j)
    else:  # 密文值在中心值右边
        D = []
        for i in range(x + 1, max(_D) + 1):
            D.append(i)
        R = []
        for j in range(center + 1, max(_R) + 1):
            R.append(j)
    return Dnc2(key_table, D, R, m)



def search(key_table1,m):#对于给定的明文范围，查找对应的密文
    list_one = readCsv(key_table)
    result1=[]
    for i in range(m[0],m[1]+1):
        for j in range(len(list_one)):
          if str(int(i))==list_one[j][1]:
            result1.append(int(list_one[j][0]))
            #result2.append(int(list_one[j][1]))
            #print(int(list_one[j][0]))
    return result1


if __name__ == '__main__':
    # D是明文域的大小
    D = []
    for i in range(999999):
        D.append(i + 1)
    # R是密文域的大小
    R = []
    for i in range(9999999):
        R.append(i + 1)
    while (1):
        print("\n"
              "\t1、加密\n"  
              "\t2、解密\n"
              )
        flag = input("请输入你要操作的编号：")
        if flag == "1":
            m=np.loadtxt(inputdata)
            # m = np.loadtxt('test.txt')
            # 从文本文件加载明文数据。文本文件中的每一行必须具有相同数量的值。
            print(m)
            x=len(m)
            result=[]
            # # D是明文域的大小
            # D = []
            # for i in range(999999):
            #     D.append(i + 1)
            # # R是密文域的大小
            # R = []
            # for i in range(9999999):
            #     R.append(i + 1)
            for i in range(x):
              result.append(Enc2(key_table, D, R, int(m[i])))
            # 打印密文
            for i in range(len(result)):
                print(result[i])
        if flag == "2":
            print("请输入需要解密的密文\n")
            m=[int(n) for n in input().split()] #m接受查询范围
            plaintext = []
            for i in range(len(m)):
                plaintext.append(Dnc2(key_table, D, R, int(m[i])))# 对result[]中每一个密文进行解密，解密后的结果存在plaintext[]中
            for i in range(len(plaintext)):
                print(plaintext[i]) 
            # print("请输入查询范围：")
            # plaintext=[]
            # m=[int(n) for n in input().split()] #m接受查询范围
            # result=search(key_table1, m)  #result[]为查询后的密文集
            # print("查询到的密文为：")
            # for i in range(len(result)):
            #   print(result[i])
            # D = []
            # for i in range(1000):
            #     D.append(i + 1)
            # R = []
            # for i in range(10000):
            #     R.append(i + 1)
            # print("解密以后的明文是：")
            # for i in range(len(result)):
            #  plaintext.append(Dnc2(key_table, D, R, int(result[i])))# 对result[]中每一个密文进行解密，解密后的结果存在plaintext[]中
            # for i in range(len(plaintext)):
            #   print(plaintext[i])