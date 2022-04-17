from time import *
import threading
import sys
import os
import struct
import socket
from AES import DECRYPT

from importlib_metadata import files

from AES import AES

def socket_service():
    host = ''
    port = 11000
    ADDR = (host, port)
    BUFSIZ = 1024

    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    # 绑定地址到套接字
    tcpSocket.bind(ADDR)
    #set the max number of tcp connection
    tcpSocket.listen(5)

    print('waiting for connection...')

    while True:
        # 被动接受TCP客户端连接,(阻塞式)等待连接的到来
        clientSocket, clientAddr = tcpSocket.accept()
        t = threading.Thread(target=deal_data,args=(clientSocket,clientAddr))
        t.start()

def deal_data(conn,addr):
    print('Accept new connection from{0}'.format(addr))
    conn.send('Welcome to the server!'.encode('utf-8'))
    while True:
        fileinfo_size = struct.calcsize('128sl')
        buf = conn.recv(fileinfo_size)
        if buf:
            filename,filesize = struct.unpack('128sl',buf)
            fn = filename.strip('\00'.encode('utf-8'))
            strfn = str(fn,'utf-8')
            # new_filename = os.path.join('./','receive_'+strfn)# fn
            new_filename = os.path.join('F:\\py-test\\'+'receive_'+strfn)
            # "C:\Users\孙玉琪\receive_info.txt"
            print('file new name is{0},filesize is{1}'.format(new_filename,filesize))
            # 记录已接收文件的大小
            recvd_size = 0
            # fp = open(new_filename,'wb')
            fp = open(new_filename,'wb+')
            print('start receiving')

            while True:
                data = conn.recv(1024)
                if not data:
                    print('end receive...')
                    break
                # data = AES('1234567890123456',str(data,'utf-8'),DECRYPT)# 在这里加上解密
                data = AES('1234567890123456',bytes.decode(data),DECRYPT)# 在这里加上解密
                print(data)
                recvd_size = recvd_size+len(data)
                # fp.write(data.encode('utf-8'))
                fp.write(data.encode())
            fp.close()
            print('end receive...')
        conn.close()
        break

if __name__ == '__main__':
    socket_service()



#     while True:
#         try:
#             # 接收 TCP 数据，数据以字符串形式返回，bufsize 指定要接收的最大数据量。
#             # flag 提供有关消息的其他信息，通常可以忽略。
#             data = clientSocket.recv(BUFSIZ)
#         except IOError as e:
#             print(e)
#             clientSocket.close()
#             break
#         if not data:
#             break
#         returnData = ctime()+data.decode('utf-8')
#         # 发送 TCP 数据，将 string 中的数据发送到连接的套接字。
#         # 返回值是要发送的字节数量，该数量可能小于 string 的字节大小。
#         clientSocket.send(returnData.encode('utf-8'))
#         if data == 'q':
#             clientSocket.close()
#     clientSocket.close()
# tcpSocket.close()