from cProfile import label
import numpy as np
import matplotlib.pyplot as plot
import time
from progress.bar import Bar
from scipy import spatial
from pyope.ope import OPE,ValueRange
# 初始化OPE类
cipher = OPE(b'long key'*2,in_range=ValueRange(0,1000000),out_range=ValueRange(0,10000000))
assert 0<cipher.encrypt(10)<cipher.encrypt(100)<10000000

import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

# 存储的是数据集中的数据加密后的结果
encrypt_x = r'F:/大数据安全/第二次实验/实验代码/encrypt_x.txt'
encrypt_y = r'F:/大数据安全/第二次实验/实验代码/encrypt_y.txt'
# mode 5会用到的list变量
x_p_list = []
y_p_list = []
x_c_list = []
y_c_list = []

# 读入数据集并将数据扩大1000000倍
def readPlaintext(plaintext_file_path):
    list_NE = [[],[]]
    with open(plaintext_file_path,'r') as fread:
        for eachline in fread:
            info = eachline.split()
            infoX = int(float(info[0])*1e6)
            infoY = int(float(info[1])*1e6)
            list_NE[0].append(infoX)
            list_NE[1].append(infoY)
    return list_NE

def KDTree_search(inputX,inputY,output):
    # 加密
    X = cipher.encrypt(inputX)
    Y = cipher.encrypt(inputY)

    # 求解明文的k近邻
    plaintext_pos = np.array([inputX,inputY],dtype=np.float64)
    # spatial.KDTree.query:Query the kd-tree for nearest neighbors.
    # print(tree_P.query(plaintext_pos))
    # 返回两个数，第一个数是该点和base点之间的距离，第二个参数是该点在KDTtree中的下标
    distance_p,index_p = tree_P.query(plaintext_pos)
    x_p = tree_P.data[index_p][0]
    y_p = tree_P.data[index_p][1]

    # 求解密文的k近邻
    ciphertext_pos = np.array([X,Y],dtype=np.float64)
    distance_c,index_c = tree_C.query(ciphertext_pos)
    x_c = tree_C.data[index_c][0]
    y_c = tree_C.data[index_c][1]
    # 得到密文域的k近邻之后再解密回明文域
    x_c = cipher.decrypt(int(x_c))
    y_c = cipher.decrypt(int(y_c))

    # 计算密文和明文到base点的欧氏距离之比，量化误差
    ratio = (np.linalg.norm([x_c-inputX,y_c-inputY]))/np.linalg.norm([x_p-inputX,y_p-inputY])

    # 打印结果
    if output:
        print("The nearest neighbor coordinates for the plaintext solution are({0},{1})".format(x_p,y_p))
        print("The nearest neighbor coordinates of the ciphertext solution are({0},{1})".format(x_c,y_c))
    else:
        plot.plot([inputX/1e6,x_p/1e6],[inputY/1e6,y_p/1e6],'y')
        plot.plot([inputX/1e6,x_c/1e6],[inputY/1e6,y_c/1e6],'g')
        x_p_list.append(inputX/1e6)
        y_p_list.append(inputY/1e6)
        x_c_list.append(x_p/1e6)
        y_c_list.append(y_p/1e6)
    return ratio



if __name__ == "__main__":
    # 首先读取测试集数据
    list_NE = readPlaintext("NE.txt")
    # print(list_NE)
    result_x = np.loadtxt(encrypt_x,int)
    result_y = np.loadtxt(encrypt_y,int)

    # 数据可视化部分
    fig = plot.figure()
    # plot.xlabel('X*1e6')
    # plot.ylabel('Y*1e6')
    # plot.scatter(list_NE[0],list_NE[1],c = 'b',marker='+')
    # plot.show()

    # KD_tree明密文索引建立，这里先建立明文的索引，密文的索引放到mode 3写
    # 但是加密的过程比较慢，为了实验演示方便，在这里用提前加密好的密文就建立索引
    tree_P = spatial.KDTree(list(zip(list_NE[0],list_NE[1])))
    tree_C = spatial.KDTree(list(zip(result_x,result_y)))

    while True:
        print("===============================================")
        print("mode 1 information encryption(int)")
        print("mode 2 information decryption")
        print("mode 3 dataset encryption")
        print("mode 4 One-shot k-nearest neighbor")
        print("mode 5 Multiple k-nearest neighbors")
        print("mode 6 quit")
        print("===============================================")
        mode = input("Please select the mode\n")
        if mode == "1":
            print("Please enter the coordinates to be encrypted(int):")
            inputX = int(input())
            inputY = int(input())
            outputX = cipher.encrypt(inputX)
            outputY = cipher.encrypt(inputY)
            print("the result is({0},{1})".format(outputX,outputY))
        if mode == "2":
            print("Please enter the coordinates to be decrypted(int):")
            inputX = int(input())
            inputY = int(input())
            outputX = cipher.decrypt(inputX)
            outputY = cipher.decrypt(inputY)
            print("the result is({0},{1})".format(outputX,outputY))
        if mode == "3":
            result_x = []
            result_y = []
            # 加个进度条
            bar_x = Bar("encrypting X",max = len(list_NE[0]),suffix = "%(percent)d%%")
            cnt = 0
            for i in bar_x.iter(list_NE[0]):
                result_x.append(cipher.encrypt(i))
            bar_y = Bar("encrypting Y",max = len(list_NE[1]),suffix = "%(percent)d%%")
            for i in bar_y.iter(list_NE[1]):
                result_y.append(cipher.encrypt(i))
        
            # 建立密文的索引，明文索引为了避免多次建立影响程序效率，已经在循坏外建立了
            tree_C = spatial.KDTree(list(zip(result_x,result_y)))

            # 保存密文
            np.savetxt(encrypt_x,result_x,fmt='%d')
            np.savetxt(encrypt_y,result_y,fmt='%d')

        if mode == "4":
            inputdata = input("Please input the base x,the default value of x is 0.5*1e6\n")
            if len(inputdata) == 0:
                inputX = int(0.5*1e6)
            else:
                inputX = int(inputdata)
            inputdata = input("Please input the base y,the default value of y is 0.5*1e6\n")
            if len(inputdata) == 0:
                inputY = int(0.5*1e6)
            else:
                inputY = int(inputdata)
            print("The center coordinates are({0},{1})".format(inputX,inputY))
            # 调用KDTree_search函数查找k近邻并返回比率
            print("ratio:",KDTree_search(inputX,inputY,1))
        
        if mode == "5":
            # 此功能不可交互，仅仅用来计算保序加密的k近邻求解准确度
            x_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
            y_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
            
            # mode 5会用到的list变量
            x_p = []
            y_p = []
            x_c = []
            y_c = []
            ratio = 0
            bar_x = Bar("searching X",max = len(x_list),suffix = "%(percent)d%%")
            for x in bar_x.iter(x_list):
            # for x in x_list:
                x = int(x*1e6)
                for y in y_list:
                    y = int(y*1e6)
                    ratio = ratio+KDTree_search(x,y,0)

            print(ratio/(len(x_list)*len(y_list)))

            # 绘制图像
            plot.xlabel('X')
            plot.ylabel('Y')
            plot.scatter(x_p_list,y_p_list,c='r',marker='+',label = 'basic point')
            plot.scatter(x_c_list,y_c_list,marker='*',label = 'near point')
            plot.legend()
            plot.show()

        if mode == "6":
            print("see you next time!\n")
            break

        if mode == "7":
            inputdata = input("Please input the base x,the default value of x is 0.5*1e6\n")
            if len(inputdata) == 0:
                inputX = int(0.5*1e6)
            else:
                inputX = int(inputdata)
            inputdata = input("Please input the base y,the default value of y is 0.5*1e6\n")
            if len(inputdata) == 0:
                inputY = int(0.5*1e6)
            else:
                inputY = int(inputdata)
            k = input("input k")
            k = int(k)
            # 加密
            X = cipher.encrypt(inputX)
            Y = cipher.encrypt(inputY)

            # 求解明文的k近邻
            plaintext_pos = np.array([inputX,inputY],dtype=np.float64)
            # spatial.KDTree.query:Query the kd-tree for nearest neighbors.
            # print(tree_P.query(plaintext_pos))
            # 返回两个数，第一个数是该点和base点之间的距离，第二个参数是该点在KDTtree中的下标
            distance_p,index_p = tree_P.query(plaintext_pos,k)
            for elem in index_p:
                x_p = tree_P.data[index_p][0]
                y_p = tree_P.data[index_p][1]
            
            print(x_p,y_p)

            # 求解密文的k近邻
            ciphertext_pos = np.array([X,Y],dtype=np.float64)
            distance_c,index_c = tree_C.query(ciphertext_pos,k)
            for elem in index_p:
                x_c = tree_C.data[index_c][0]
                y_c = tree_C.data[index_c][1]

            print(x_p,y_p)