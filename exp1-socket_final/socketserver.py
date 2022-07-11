from math import floor
from statistics import mode
from time import *
import threading
import sys
import os
import struct
import socket
from myAES import DECRYPT
from DH.DH import DH, find_pg
from DH import User
from DH.MD5 import MD5
from myAES import AES as myAES
from Crypto.Cipher import AES

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
    socket.setdefaulttimeout(500)

    print('waiting for connection...')

    while True:
        # 被动接受TCP客户端连接,(阻塞式)等待连接的到来
        clientSocket, clientAddr = tcpSocket.accept()
        t = threading.Thread(target=deal_data,args=(clientSocket,clientAddr))
        t.start()

def deal_data(conn,addr):
    print('Accept new connection from{0}'.format(addr))
    conn.send('Welcome to the server!Let\'s exchange the key'.encode('utf-8'))
    p,g = find_pg()
    Server = DH(p,g)
    p_g_publicKey = str(p)+'A'+str(g)+'A'+str(Server.send_to_other_key)
    conn.send(p_g_publicKey.encode())
    # conn.send('Server\'s public key send over'.encode())
    data = conn.recv(1024)
    public_key = int(data)
    Server.calculateAESKey(public_key)
    conn.send('key exchange completed'.encode())
    print('The server\'s AES key seed is '+str(Server.AES_key))
    Servermd5 = MD5(str(Server.AES_key))
    key = Servermd5.md5Encode()
    print('The server\'s AES key is '+key)
    # while True:
    data = conn.recv(1024)
    data = data.strip('\00'.encode('utf-8'))
    str_mode = data.decode()
    mode = str_mode
    conn.send('get mode sucessfully'.encode())
    fileinfo_size = struct.calcsize('128sl')
    buf = conn.recv(fileinfo_size)
    if buf:
        filename,filesize = struct.unpack('128sl',buf)
        # if filesize%16!=0:
        #     filesize = filesize+16 # 因为AES加密会填充够16个
        #     filesize = int(floor(filesize/16)*16)
        fn = filename.strip('\00'.encode('utf-8'))
        strfn = str(fn,'utf-8')
        new_filename = os.path.join('F:\\py-test\\key_exchange\\'+'receive_'+strfn)
        print('file new name is{0},filesize is{1}'.format(new_filename,filesize))
        # 记录已接收文件的大小
        recvd_size = 0
        fp = open(new_filename,'wb+')
        print('start receiving')
        if not mode == 'img':
            while not recvd_size == filesize:
                # 可能会碰到ConnectionResetError [WinError 10054] 远程主机强迫关闭了一个现有的连接。这是因为client已经发完数据并关闭了连接造成的
                if filesize -recvd_size >1024:
                    data = conn.recv(1024)
                    try:
                        strdata = data.decode()
                    except UnicodeDecodeError:
                        adddata = conn.recv(1)
                        data = data+adddata
                    recvd_size = recvd_size+len(data)
                    data = myAES(key,data.decode(),DECRYPT)# 在这里加上解密
                    # print(data)
                    fp.write(data.encode())
                    conn.send('success receive...'.encode())
                else:
                    data = conn.recv(filesize-recvd_size)
                    recvd_size = recvd_size+len(data)
                    data = myAES(key,data.decode(),DECRYPT)# 在这里加上解密
                    # print(data)
                    fp.write(data.encode())
                    conn.send('success receive...'.encode())
                # 如果要实现同一文件多次加密结果不同，取消下列注释
                # key = Servermd5.md5Encode()
        else:# edit
            while not recvd_size == filesize:
                # 可能会碰到ConnectionResetError [WinError 10054] 远程主机强迫关闭了一个现有的连接。这是因为client已经发完数据并关闭了连接造成的
                if filesize -recvd_size >1024:
                    data = conn.recv(1024)
                    recvd_size = recvd_size+len(data)
                    key_byte = key.encode()
                    key_16 = key_byte[0:16]
                    password = b'1234567812345678'
                    aes = AES.new(key_16,AES.MODE_ECB) #创建一个aes对象 在这里加上解密
                    de_data = aes.decrypt(data)
                    # print(data)
                    fp.write(de_data)
                    conn.send('success receive...'.encode())
                else:
                    data = conn.recv(filesize-recvd_size)
                    recvd_size = recvd_size+len(data)
                    key_byte = key.encode()
                    key_16 = key_byte[0:16]
                    password = b'1234567812345678'
                    aes = AES.new(key_16,AES.MODE_ECB) #创建一个aes对象 在这里加上解密
                    de_data = aes.decrypt(data)
                    # print(data)
                    fp.write(de_data)
                    conn.send('success receive...'.encode())
        fp.close()
        print('end receive...')
        # conn.send('receive successfully'.encode())
    conn.close()

if __name__ == '__main__':
    socket_service()


# 104651014