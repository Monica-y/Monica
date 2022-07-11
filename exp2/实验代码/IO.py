from position import position
# 因为浮点数缺乏精准性，所以我对数据集数据进行同比例放大，在以后的程序中使用整数来处理数据
class IO:
    # 数据放大倍数
    proportion = 1
    # 明文文件路径(读)
    plaintext_file_path = ''
    # 密码表路径(写读) 密文-明文
    password_table_path = ''

    def __init__(self,proportion,plaintext_file_path,password_table_path) -> None:
        self.proportion = proportion
        self.plaintext_file_path = plaintext_file_path
        self.password_table_path = password_table_path
    
    def readPlaintext(self):
        list_location = []
        with open(self.plaintext_file_path,'r') as fread:
            for eachline in fread:
                info = eachline.split()
                finfoX = float(info[0])*self.proportion
                finfoY = float(info[1])*self.proportion
                iinfoX = int(finfoX)
                iinfoY = int(finfoY)
                list_location.append(position(iinfoX,iinfoY))
        return list_location
    # 存储的是密文明文对
    def writePassword(self,info):
        cnt = 0
        with open(self.password_table_path,'a') as fwrite:
            for elem in info:
                fwrite.write(str(elem.x)+' '+str(elem.y)+'\n')

    # 如果有记录，返回的是一个正整数，表示密文对应的明文，否则返回-1
    def searchPassword(self,aim):
        straim = str(aim)
        with open(self.password_table_path,'r') as fread:
            for eachline in fread:
                info = eachline.split()
                if len(info) == 0:
                    return -1
                if info[0] == straim:
                    return int(info[1])
        return -1

if __name__ == "__main__":

    datasetIO = IO(1000000,"NE.txt","password_table.txt")
    list_location = datasetIO.readPlaintext()
    # for elem in list_location:
    #     elem.print_pos()
    # datasetIO.writePassword(list_location)
    print(datasetIO.searchPassword(354778))