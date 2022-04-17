from socket import *
import os
import sys
import struct
from AES import AES
from AES import ENCRYPT
from urllib import parse
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

    while True:
        # data = "client message"
        # data = input('>>>')
        filepath = input("please input file path:")
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包括文件名和文件大小
            fhead = struct.pack('128sl',os.path.basename(filepath).encode('utf-8'),
            os.stat(filepath).st_size)
            clientSocket.send(fhead)
            print('client filepath:{0}'.format(filepath))
            fp = open(filepath,'rb')
            # fp = open(filepath,'r')
            while True:
                data = fp.read(1024)# 1024
                # data = AES('1234567890123456',str(data,'utf-8'),ENCRYPT)
                if not data:
                    print('{0} file send over...'.format(filepath))
                    break
                data = AES('1234567890123456',bytes.decode(data),ENCRYPT)      
                # clientSocket.send(data.encode('utf-8'))
                clientSocket.send(data.encode())
        # clientSocket.send(data.encode('utf-8'))
        # returnData = clientSocket.recv(BUFSIZ)
        # if not returnData:
        #     break
        # print('Return time is:%s' %returnData.decode('utf-8'))
        clientSocket.close()

if __name__ == '__main__':
    socket_client()