import csv
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial
from pyope.ope import OPE, ValueRange
cipher = OPE(b'long key' * 2, in_range=ValueRange(0, 1000000),
             out_range=ValueRange(0, 10000000))
assert 0 < cipher.encrypt(10) < cipher.encrypt(42) < 9999
# OPE

key_table = "data_c.csv"
encrypt_x = r'F:/大数据安全/第二次实验/实验代码/encrypt_x.txt'
encrypt_y = r'F:/大数据安全/第二次实验/实验代码/encrypt_y.txt'


def writeCsv(path, data, modle):  # 传入变量csv文件的路径和要写入的数据
    with open(path, modle, newline="") as f:  # 以写入的方式打开文件，newline="" 可以让数据不隔行写入
        writer_csv = csv.writer(f)  # 调用csv的writer方法往文件里面写入数据，并赋值给writer_scv变量
        writer_csv.writerow(data)  # 把数据循环写入到writer_csv变量中


def readfile(path):
    list_one = [[], []]  # 定义一个空列表
    with open(path, "r") as f:  # 以只读的方式打开文件
        read_scv = csv.reader(f)  # 调用csv的reader方法读取文件并赋值给read_scv变量
        for i in read_scv:
            list_one[0].append(float(i[0][0:8]))  # 将读取到的数据追加到list列表里面
            list_one[1].append(float(i[0][9:17]))
    return list_one  # 返回列表数据


def pre_op(list_0):
    # list_0中元素都扩展成1e6倍
    list_new = [[], []]
    list_new[0] = list(map(lambda x: int(x*1e6), list_0[0]))
    list_new[1] = list(map(lambda x: int(x*1e6), list_0[1]))
    return list_new


if __name__ == '__main__':
    # readfile
    # list_0 = readfile("E:/大三下学期学习/大数据安全与隐私/试验2/dataset/NE/NE.txt")
    list_0 = readfile("NE.txt")
    list_new = pre_op(list_0)
    result_x = np.loadtxt(encrypt_x, int)
    result_y = np.loadtxt(encrypt_y, int)

    # plot
    fig = plt.figure()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.scatter(list_0[0], list_0[1], c='b', marker='*')

    # KD_tree明秘密文索引建立
    tree_P = spatial.KDTree(list(zip(list_new[0], list_new[1])))
    tree_C = spatial.KDTree(list(zip(result_x, result_y)))

    # 明文最近邻查询，可以循环多组

    while (1):
        print("=================\n"
              "\t1、加密\n"
              "\t2、解密\n"
              "\t3、NE dataset 二维加密(!)\n"
              "\t4、单次计算ratio\n"
              "\t5、循环计算ratio\n"
              "=================")
        flag = input("请输入你要操作的编号：")
        if flag == "1":
            print("请输入你要加密的坐标")
            find_a = int(float(input())*1e6)
            find_b = int(float(input())*1e6)
            print("你要加密的坐标为(%.6f,%.6f)" % (find_a/1e6,find_b/1e6))
            x = cipher.encrypt(find_a)
            y = cipher.encrypt(find_b)
            print("加密后坐标为    (%.6f,%.6f)" % (x/1e6,y/1e6))
        if flag == "2":
            print("请输入你要解密的坐标")
            find_a = int(float(input())*1e6)
            find_b = int(float(input())*1e6)
            print("你要解密的坐标为(%.6f,%.6f)" % (find_a/1e6,find_b/1e6))
            x = cipher.decrypt(find_a)
            y = cipher.decrypt(find_b)
            print("解密后坐标为    (%.6f,%.6f)" % (x/1e6,y/1e6))
        if flag == "3":
            result_x = []
            result_y = []
            num = 0
            start = time.time()
            for i in list_new[0]:
                result_x.append(cipher.encrypt(i))
                num = num + 1
                if num % 10000 == 0:
                    print(num)
            num = 0
            end1 = time.time()
            #print("run time :  \n",end1-start)

            for i in list_new[1]:
                result_y.append(cipher.encrypt(i))
                num = num + 1
                if num % 10000 == 0:
                    print(num)

            end2 = time.time()
            print("run time :  \n", end2-end1)

            np.savetxt(
                r'E:/大三下学期学习/大数据安全与隐私/试验2/download/pyope/data_c_x.txt', result_x, fmt='%d')
            np.savetxt(
                r'E:/大三下学期学习/大数据安全与隐私/试验2/download/pyope/data_c_y.txt', result_y, fmt='%d')

        if flag == "4":
            # 单次加密
            #default value (0.5,0.5)
            find_a = 0.5*1e6
            find_b = 0.5*1e6
            ratio = 0
            while(1):
                find_a = int(float(input())*1e6)
                find_b = int(float(input())*1e6)
                print("你指定的坐标为(%.6f,%.6f)" % (find_a/1e6,find_b/1e6))
                x = cipher.encrypt(find_a)
                y = cipher.encrypt(find_b)
                print("加密后坐标为    (%.6f,%.6f)" % (x/1e6,y/1e6))
                # p
                pts = np.array([find_a, find_b])
                d_p, index_p = tree_P.query(pts)
                # print(tree_P.query(pts))
                r_x = int(tree_P.data[index_p][0])  # 最近邻x坐标转化后
                r_y = int(tree_P.data[index_p][1])  # 最近邻y坐标转化后
                # c
                pts_c = np.array([cipher.encrypt(find_a), cipher.encrypt(find_b)])
                d_c, index_c = tree_C.query(pts_c)
                s_x = cipher.decrypt(int(tree_C.data[index_c][0]))  # 密文最近邻x坐标转化后
                s_y = cipher.decrypt(int(tree_C.data[index_c][1]))  # 密文最近邻y坐标转化后
                # 计算ratio 明密文欧氏距离之比
                ratio = (np.linalg.norm([s_x-find_a, s_y-find_b], ord=2)
                )/(np.linalg.norm([r_x-find_a, r_y-find_b]))
                
                print("最近邻原坐标:(%.6f,%.6f)" % (r_x/1e6,r_y/1e6))
                print("加密后最近邻坐标:(%.6f,%.6f)" % (tree_C.data[index_c][0]/1e6,tree_C.data[index_c][1]/1e6))
                print("ratio: ",ratio)
                break
        if flag == "5":
            #循环加密
            #default value (0.5,0.5)
            find_a = 0.5*1e6
            find_b = 0.5*1e6
            x_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
            y_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]


            b_x = [] #basic point
            b_y = []
            c_x = [] #closest point
            c_y = []
            ratio = 0
            count = 0
            plt.figure()
            for find_a in x_list:
                
              find_a = int(find_a*1e6)
              for find_b in y_list:

                find_b = int(find_b*1e6)
                print("你指定的坐标为(%.6f,%.6f)" % (find_a/1e6,find_b/1e6))
                x = cipher.encrypt(find_a)
                y = cipher.encrypt(find_b)
                print("加密后坐标为  (%.6f,%.6f)" % (x/1e6,y/1e6))

                # p
                pts = np.array([find_a, find_b])
                d_p, index_p = tree_P.query(pts)
                r_x = int(tree_P.data[index_p][0])  # 最近邻x坐标转化后
                r_y = int(tree_P.data[index_p][1])  # 最近邻y坐标转化后
                # c
                pts_c = np.array([cipher.encrypt(find_a), cipher.encrypt(find_b)])
                d_c, index_c = tree_C.query(pts_c)
                s_x = cipher.decrypt(int(tree_C.data[index_c][0]))  # 密文最近邻x坐标转化后
                s_y = cipher.decrypt(int(tree_C.data[index_c][1]))  # 密文最近邻y坐标转化后
                # 计算ratio
                ratio = ratio + (np.linalg.norm([s_x-find_a, s_y-find_b], ord=2)
                )/(np.linalg.norm([r_x-find_a, r_y-find_b]))
                count = count + 1
                print("最近邻原坐标:    (%.6f,%.6f)" % (r_x/1e6,r_y/1e6))
                print("加密后最近邻坐标:(%.6f,%.6f)\n" % (tree_C.data[index_c][0]/1e6,tree_C.data[index_c][1]/1e6))
                #plot
                plt.plot([find_a/1e6, r_x/1e6],[find_b/1e6, r_y/1e6],'y')
                b_x.append(find_a/1e6)
                b_y.append(find_b/1e6)
                c_x.append(r_x/1e6)
                c_y.append(r_y/1e6)
            
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.scatter(b_x, b_y, c='r', marker='*',label = 'basic point')
            plt.scatter(c_x, c_y, c='b', marker='*', label = 'closest point') 
            plt.legend()    
            plt.show()
            print("count: ",count)
            print("ratio: ",ratio/count)