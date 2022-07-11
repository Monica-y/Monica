from multiprocessing.connection import Client
from socket import *
import os
import sys
import struct
from AES import AES
from AES import ENCRYPT
from urllib import parse
from DH import User
from DH.DH import DH
from DH.MD5 import MD5
from getlen import getlen
def socket_client():
    serverName = '127.0.0.1'
    serverPort = 11000
    BUFSIZ = 1024
    ADDR = (serverName,serverPort)
    # 套接字家族可以使 AF_UNIX 或者 AF_INET。
    # 套接字类型可以根据是面向连接的还是非连接分为 SOCK_STREAM 或 SOCK_DGRAM。
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # 主动初始化TCP服务器连接。
    # 一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。
    clientSocket.connect(ADDR)
    print(clientSocket.recv(BUFSIZ))
    data = clientSocket.recv(BUFSIZ)
    str_data = bytes.decode(data)
    # p_g_public
    begin = 0
    keyword = ['','','']
    cnt = 0
    for index in range(len(str_data)):
        if str_data[index] == 'A'or index == len(str_data)-1:
            if(index == len(str_data)-1):
                index = index+1
            for i in range(begin,index):
                keyword[cnt] = keyword[cnt]+str_data[i]
            cnt = cnt+1
            begin = index+1
    client = DH(int(keyword[0]),int(keyword[1]))
    client.calculateAESKey(int(keyword[2]))
    clientSocket.send(str(client.send_to_other_key).encode())
    print(clientSocket.recv(BUFSIZ))
    print('The client\'s AES key seed is '+str(client.AES_key))
    Clientmd5 = MD5(str(client.AES_key))
    key = Clientmd5.md5Encode()
    print('The client\'s AES key is '+key)
    while True:
        filepath = input("please input file path:")
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包括文件名和文件大小
            datalen = getlen(filepath,key)
            fhead = struct.pack('128sl',os.path.basename(filepath).encode('utf-8'),
           datalen)
        if os.path.isfile(filepath):
            clientSocket.send(fhead)
            print('client filepath:{0}'.format(filepath))
            fp = open(filepath,'rb')
            while True:
                data = fp.read(256)
                if not data:
                    print('{0} file send over...'.format(filepath))
                    fp.close()
                    break
                data = AES(key,bytes.decode(data,'utf-8','ingore'),ENCRYPT)      
                clientSocket.send(data.encode())
                print(clientSocket.recv(BUFSIZ)) # edit
    # 因为如果传输完数据就关闭client，那么server那里会报错，因此使用死循环让client不能断开，这样server就不会报错了
    clientSocket.close()

if __name__ == '__main__':
    socket_client()