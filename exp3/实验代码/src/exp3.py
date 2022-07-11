import sys
import os

import matplotlib.pyplot as plot
# 程序运行的根路径
sys.path.append("F:\\大数据安全\\第三次实验\\实验代码")
from utilis.readdata import *
from k_anonymity import KAnonymity
import numpy as np
import math

# 计算平均年龄 Calculate the average age
def calculate_avgage(filepath = "F:\\大数据安全\\第三次实验\\实验代码\\data", filename = "",type = "",dellist = []):
    """
    参数
        type = 1,计算泛化后的数据集的平均年龄
        type = 2,计算原始数据集的平均年龄
    返回值
        一个float值,表示平均值
    """
    data = []
    with open(os.path.join(filepath,filename),'r') as readfile:
        for line in readfile:
            # 去掉行尾空格
            line = line.strip()
            if not line:
                continue
            line = [elem.strip() for elem in line.split(',')]
            # 如果是要计算泛化后的平均值
            if type == 1:
                textline = []
                # 这里的目标是age字段
                textline = line[0].split('-')
                data.append((int(textline[0])+int(textline[1]))/2.0)
            # 如果是要计算原始数据的平均年龄
            elif type == 2:
                data.append(int(line[0]))
        if len(dellist)!=0:
            for i in dellist:
                del data[i]
    return sum(data)/len(data)

# Laplace噪声
class Laplace():
    def __init__(self,records):
        self.records = records
        self.s = self.calculate_sensitivity()

    def calculate_sensitivity(self,above_age = 1):
        """
        计算Laplace的敏感度参数,公式是 最大值/数据数
        """
        num,oldest = 0,-float('inf')
        ageidx = ATTNAME.index('age')
        for record in self.records:
            if(record[ageidx]>above_age):
                num = num+1
                if record[ageidx]>oldest:
                    oldest = record[ageidx]
        return oldest/num
    
    # 添加Laplace噪声
    def laplace_noise(self,e):
        '''
        add laplace noise
        '''
        return np.random.laplace(self.s/e)

    # Laplace处理
    def query(self,e = 1,querynum = 1000,above_age = 1):
        """
        参数
            e是Laplace参数
            querynum是询问的次数
        返回值
            返回随即查询结果
        """

        ageidx = ATTNAME.index('age')
        agelist = [record[ageidx] for record in self.records if record[ageidx]>above_age]
        avg_age = sum(agelist)/len(agelist)

        result = []
        for i in range(querynum):
            # 保留一位小数
            result.append(round(avg_age+self.laplace_noise(e),1))
        return result



if __name__ == "__main__":
    # 需要注意的是进行差分攻击，必须要有两组平均数的查询结果，且得到第二组结果之前，必须删掉一条数据，才能用于构建差分攻击
    # 初始化k匿名算法参数
    k = 5
    # 真实数据的平均值
    real_avg_age = 0
    # 用于记录删掉的元素，来进行差分攻击
    delist = []
    # 画图所用list
    xlist = []
    ylist = []
    # 记录绘图所用数据的dict
    data = {}
    while True:
        print("==========================================")
        print("mode 0 quit")
        print("mode 1 k-Anonymize the dataset adult.data")
        print("mode 2 Differential attack using real data average")
        print("mode 3 Differential attack using laplace data average")
        print("mode 4 Differential attack using k-anonymize data average")
        print("mode 5 Comparison of three mean query results")
        print("==========================================")
        # 先读入数据集数据,返回一个list
        records = readdata()
        mode = input("Please select a mode\n")
        # 程序退出
        if mode == '0':
            print("see you next time!")
            break
        # k匿名处理
        elif mode == '1':
            k = input("Please enter a value for k\n")
            k = int(k)
            # 使用数据集数据创建KAnonymity对象
            KAnony = KAnonymity(records)
            # 对age，education数据进行脱敏，参数为k
            # 函数将处理结果写在"F:\大数据安全\第三次实验\实验代码\data\adult_k_kanonymity.data"路径
            KAnony.anonymize(qi_names=['age','education'],k=k)
            print("k Anonymous processing completed!")
        # 使用真实数据的平均值进行的差分攻击
        elif mode == '2':
            # 从k匿名处理前的数据中计算出真实的平均年龄
            # real_avg_age1 = calculate_avgage(filepath='./data',filename='adult.data',type=2)
            real_avg_age1 = calculate_avgage(filepath="F:\\大数据安全\\第三次实验\\实验代码\\data",filename='adult.data',type=2)
            print("目前的平均年龄是{}".format(real_avg_age1))
            xlist = []
            ylist = []
            ylist.append(real_avg_age1)
            data['real'] = real_avg_age1
            # 删除掉一个数据
            delrecord = int(input("Please enter the data index to delete\n"))
            delist.append(delrecord)
            if len(delist)!=0:
                for i in delist:
                    print("Dropped index is {}, age is {}".format(i,records[i][0]))
                    # 删除list中对应的内容
                    del records[i]
            # 再次计算真实的平均年龄
            # real_avg_age2 = calculate_avgage(filepath='./data',filename='adult.data',type=2,dellist=delist)
            real_avg_age2 = calculate_avgage(filepath="F:\\大数据安全\\第三次实验\\实验代码\\data",filename='adult.data',type=2,dellist=delist)
            print("目前的平均年龄是{}".format(real_avg_age2))
            age_delete = real_avg_age1*(len(records)+len(delist))-real_avg_age2*len(records)
            print("Use differential attack to get deleted records's age {}".format(age_delete))
            # 攻击结束之后将dellist清空
            if len(delist)>0:
                del delist[0]

        # 使用经过Laplace噪声处理过的数据均值
        # 知乎里有多少人是985大学毕业的？假如真实结果是2000人，那么每一次查询得到的结果都会稍稍有些区别，比如有很高的概率输出2001，也较高概率输出2010，很低概率输出1000
        elif mode == '3':
            Lap1 = Laplace(records)
            querynum = 800
            query1 = Lap1.query(0.8,querynum,above_age=1)
            avg_age_lap1 = sum(query1)/len(query1)
            print("差分隐私查询{}次的平均年龄为{}".format(querynum,avg_age_lap1))
            ylist.append(avg_age_lap1)
            data['laplace'] = avg_age_lap1
            # 删除掉一条数据
            delrecord = int(input("Please enter the data index to delete\n"))
            delist.append(delrecord)
            if len(delist)!=0:
                for i in delist:
                    print("Dropped index is {}, age is {}".format(i,records[i][0]))
                    # 删除list中对应的内容
                    del records[i]
            # 再次查询均值
            Lap2 = Laplace(records)
            query2 = Lap2.query(0.8,querynum,above_age=1)
            avg_age_lap2 = sum(query2)/len(query2)
            print("差分隐私查询{}次的平均年龄为{}".format(querynum,avg_age_lap2))
            # 差分攻击
            age_delete = avg_age_lap1*(len(records)+len(delist))-avg_age_lap2*len(records)
            print("Use differential attack to get deleted records's age {}".format(age_delete))
            # 攻击结束之后将dellist清空
            if len(delist)>0:
                del delist[0]
        # 在k匿名泛化后的数据集上进行差分攻击
        elif mode == '4':
            # avg_age_k1 = calculate_avgage(filepath = './data',filename='adult_'+str(k)+'_kanonymity.data',type=1)
            avg_age_k1 = calculate_avgage(filename='adult_'+str(k)+'_kanonymity.data',type=1)
            print("Average age after anonymity is {}".format(avg_age_k1))
            ylist.append(avg_age_k1)
            data['k-anonymity'] = avg_age_k1
            # 删除掉一条记录
            delrecord = int(input("Please enter the data index to delete\n"))
            delist.append(delrecord)
            if len(delist)!=0:
                for i in delist:
                    print("Dropped index is {}, age is {}".format(i,records[i][0]))
                    # 删除list中对应的内容
                    del records[i]
            # 再次查询均值
            # avg_age_k2 = calculate_avgage(filepath='./data',filename='adult_'+str(k)+'_kanonymity.data',type=1)
            avg_age_k2 = calculate_avgage(filename='adult_'+str(k)+'_kanonymity.data',type=1)
            print("Average age after anonymity is {}".format(avg_age_k2))
            # 差分攻击
            age_delete = avg_age_k1*(len(records)+len(delist))-avg_age_k2*len(records)
            print("Use differential attack to get deleted records's age {}".format(age_delete))
            # 攻击结束之后将dellist清空
            if len(delist)>0:
                del delist[0]
        # 比较三种均值查询结果
        elif mode == '5':
            xlist = ['real','laplace','k-anonymity']
            ylist = [data['real'],data['laplace'],data['k-anonymity']]
            plot.bar(xlist,ylist)
            plot.show()