
from re import X
import sys
import os
from os import path
import matplotlib.pyplot as plt
sys.path.append("E:\大三下学期学习\大数据安全与隐私\试验3\code\K-anonymity-and-Differential-Privacy-master\K-anonymity-and-Differential-Privacy-master")

from utilis.readdata import *
from k_anonymity import KAnonymity
import numpy as np
import math


class LaplaceMechanism():
    def __init__(self, records):
        self.records = records
        self.s = self.__calculate_sensitivity()
        # print(self.s)

    def __calculate_sensitivity(self,above_age = 25):
        """
        calculate the sensitive value
        it should be the oldest age / num of records

        Returns:
            [float] -- [sensitive value]
        """

        num, oldage = 0, -float('inf')
        ageidx = ATTNAME.index('age')
        for record in self.records:
            if record[ageidx] > above_age:
                num += 1
                if record[ageidx] > oldage:
                    oldage = record[ageidx]
        return oldage / num

    def __laplacian_noise(self, e):
        """
        add laplacian_noise
        """

        return np.random.laplace(self.s/e)

    def query_with_dp(self, e = 1, querynum=1000 , above_age = 25):
        """
        change!!!
        query average age above 25 with Laplace Mechanism
        
        Keyword Arguments:
            e {float} -- [epsilon] (default: {1})
            querynum {int} -- [number of queries] (default: {1000})
        
        Returns:
            [list] -- [randomized query results]
        """

        ageidx = ATTNAME.index('age')
        agegt25 = [record[ageidx]
                   for record in self.records if record[ageidx] > above_age]
        avgage = sum(agegt25) / len(agegt25)

        res = []
        for _ in range(querynum):
            res.append(round(avgage + self.__laplacian_noise(e), 2))
        return res

    def calc_groundtruth(self,above_age = 25):
        """
        calculate the true average age above 25 without adding noise
        
        Returns:
            [float] -- [true average age greater than 25]
        """

        agesum = 0
        num = 0
        ageidx = ATTNAME.index('age')
        for record in self.records:
            if record[ageidx] > above_age:
                agesum += record[ageidx]
                num += 1
        return round(agesum / num, 2)


    def calc_distortion(self, queryres):
        """
        calcluate the distortion
        use RMSE here
        
        Arguments:
            queryres {[list]} -- [query result]
        
        Returns:
            [float] -- [rmse value]
        """

        groundtruth = self.calc_groundtruth()
        rmse = (sum((res - groundtruth)**2 for res in queryres) / len(queryres))**(1/2)
        return rmse

def prove_indistinguishable(queryres1, queryres2, bucketnum = 20):
    """
    proove the indistinguishable for two query results
    
    Arguments:
        queryres1 {[list]} -- [query 1 result]
        queryres2 {[list]} -- [query 2 result]
    
    Keyword Arguments:
        bucketnum {int} -- [number of buckets used to calculate the probability] (default: {20})
    
    Returns:
        [float] -- [probability quotient]
    """

    maxval = max(max(queryres1), max(queryres2))
    minval = min(min(queryres1), min(queryres2))
    count1 = [0 for _ in range(bucketnum)]
    count2 = [0 for _ in range(bucketnum)]
    for val1, val2 in zip(queryres1, queryres2):
        count1[math.floor((val1-minval+1)/((maxval-minval+1)/bucketnum))-1] += 1
        count2[math.floor((val2-minval+1)//((maxval-minval+1)/bucketnum))-1] += 1
    prob1 = list(map(lambda x: x/len(queryres1), count1))
    prob2 = list(map(lambda  x: x/len(queryres2), count2))

    res1overres2 = sum(p1 / p2 for p1, p2 in zip(prob1, prob2) if p2 != 0) / bucketnum
    res2overres1 = sum(p2 / p1 for p1, p2 in zip(prob1, prob2) if p1 != 0) / bucketnum
    return res1overres2, res2overres1
def cac_avg_age(filepath='./data', filename='adult.data',type = 1,dellist = []):
    """
    caculate the average age of the whole data set with K-anoymize
    Arguments:
        type[int]: 1 -- for K-anonymize age
                   2 -- for true age
    Returns:
        [float] -- [average age of the type]
    """
    records = []
    
    with open(os.path.join(filepath, filename), 'r') as rf:
        for line in rf:
            line = line.strip()
            if not line:
                continue
            line = [a.strip() for a in line.split(',')]
            # print(line)

            if type == 1:
                if line[0]=="0-25":
                    records.append(12.5)
                elif line[0]=="25-50":
                    records.append(37.5)
                elif line[0]=="50-75":
                    records.append(62.5)
                elif line[0]=="75-100":
                    records.append(87.5)
                elif line[0]=="0-50":
                    records.append(25)
                elif line[0]=="50-100":
                    records.append(75)
            elif type == 2:
                records.append(int(line[0]))
        if len(dellist)!=0:
            for i in dellist:
                del records[i]        
    return  sum(records) / len(records)


if __name__ == "__main__":
    #注意每次执行完删除后才可以执行查询,必须是4-2/4-3才可以，不能是4-2-3连续
    #初始化参数
    k = 10
    real_avg_age = 0
    dellist = []
    # 建立字典 key value 形式，key不可以重复
    mistake = {'real':[],'k_anonymize':[],'DP':[]}
    xlist = []
    ylist = []
    while(1):
      print("=================\n"
              "\t1、K匿名 Adult.data \n" 
              "\t2、K匿名查找平均年龄 \n"
              "\t3、差分隐私查找平均年龄 \n"
              "\t4、删除某一条数据\n"
              "\t5、真实年龄平均数据\n"
              "\t0、退出\n"
              "\t(推荐执行顺序为1-5-4-5-3-4-3-2-4-2-0)\n"
              "=================")
      c = input("请输入您的操作！\n")
      # 读入信息并返回一个list
      records = readdata() 
      if len(dellist)!=0:
        for i in dellist:
          print("删除索引为{},年龄为{}".format(i,records[i][0]))
          # 删除list中对应的内容
          del records[i]

      if c == '1': ##K匿名生成

        k = int(input("请输入k值\n"))
        # 使用数据集创建KAnonymity对象
        KAnony = KAnonymity(records)
        # 对'age', 'education'数据进行脱敏，参数为k，函数将处理结果写在"F:\大数据安全\第三次实验\实验代码\data\adult_10_kanonymity.data"路径
        KAnony.anonymize(qi_names=['age', 'education'],k = k)

      if c == '2':##K匿名查找

        # print(k)
        # print(os.getcwd())
        avg_age_k = cac_avg_age(filepath='./data', filename='adult_'+str(k)+'_kanonymity.data',dellist=dellist)
        #差分攻击
        mistake['k_anonymize'].append(avg_age_k)        
        if len( mistake['k_anonymize']) == 2:                
            print("执行以上操作后K-匿名后平均年龄：\n",avg_age_k)
            age_predict = mistake['k_anonymize'][0]*(len(records)+len(dellist)) - avg_age_k*len(records)
            print("根据前后数值差分攻击得到删除掉的年龄为：\n",age_predict)
            del mistake['k_anonymize'][1]
            if len(dellist)>0:
                del dellist[0]
        else : 
            print("K-匿名后平均年龄：",avg_age_k)

      if c == '3':## laplace 查询
        
        aa = int(input("请输入您想要查询的范围(默认大于25岁)\n"))
        LapMe = LaplaceMechanism(records)
        res1 = LapMe.query_with_dp(0.5, 1000,above_age = aa)
        #画图
        delta = 0.1
        bumket = [0 for i in range(0,int(20/delta))]
        for i in res1:
            bumket[int((i-real_avg_age-10)/delta)] +=1
        x_lable = np.linspace(round(real_avg_age-10,1),round(real_avg_age+10,1),200)
        #plt.plot(x_lable,bumket,color = 'r')
        xlist.append(x_lable)
        ylist.append(bumket)
        fig, ax = plt.subplots()
        ax.plot(x_lable,bumket,color = 'r' )
        ax.set(xlabel='avrage age(year)', ylabel='count',
            title='Laplace Distribution')
        ax.grid()
        plt.show()

        avg_age_DP = sum(res1)/len(res1)
        #差分攻击
        mistake['DP'].append(avg_age_DP)        
        if len( mistake['DP']) == 2:                
            print("执行以上操作后,差分隐私后平均年龄：\n",avg_age_DP)
            age_predict = mistake['DP'][0]*(len(records)+len(dellist)) - avg_age_DP*len(records)
            print("根据前后数值差分攻击得到删除掉的年龄为：\n",age_predict)
            del mistake['DP'][1]
            if len(dellist)>0:
                del dellist[0]
            fig, ax = plt.subplots()
            line1, = ax.plot(x_lable,bumket,color = 'r' )
            line2, = ax.plot(xlist[0],ylist[0],color = 'g' )
            plt.legend((line1,line2),('now','before'))
            ax.set(xlabel='avrage age(year)', ylabel='count',
                title='Laplace Distribution')
            ax.grid()
            plt.show()
        else : 
            print("差分隐私查询1000次的均值为：",avg_age_DP)

      if c == '4':##删除一条数据

        delp = int(input("请输入要删除的索引:\n"))  
        dellist.append(delp)

      if c == '5':##真实年龄查询

        avg_age = cac_avg_age(filepath='./data', filename='adult.data',type = 2 ,dellist=dellist)  
        real_avg_age = avg_age
        
        #差分攻击
        mistake['real'].append(avg_age)        
        if len(mistake['real']) == 2:                
            print("执行以上操作后,真实平均年龄：\n",avg_age)
            age_predict = mistake['real'][0]*(len(records)+len(dellist)) - avg_age*len(records)
            print("根据前后数值差分攻击得到删除掉的年龄为：\n",age_predict)
            del mistake['real'][1]
            if len(dellist)>0:
                del dellist[0]
        else : 
            print("真实平均年龄：",avg_age)

        
      if c== '0':##退出
        break