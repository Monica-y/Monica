import os
from AES import ENCRYPT
from AES import AES

def getlen(filepath,key):
    filelen = 0
    if os.path.isfile(filepath):
        fp = open(filepath,'rb')
        while True:
            data = fp.read(512)# 1024的话这里可能会有问题,因为编码后大小会变大
            if not data:
                print('{0} End of encrypted file size calculation...'.format(filepath))
                fp.close()
                break
            data = AES(key,bytes.decode(data),ENCRYPT) 
            filelen = filelen+len(data.encode())
    # print(filelen)
    return filelen     

if __name__ == '__main__':
    len1 = getlen("F:\\py-test\\key_exchange\\history.txt",'1234567890123456')
    print(len1)
    res = AES('1234567890123456','Rather than building all of its functionality into its core, Python was designed to be highly extensible via modules. This compact modularity has made it particularly popular as a means of adding programmable interfaces to existing applications. Van Rossum\'s vision of a small core language with a large standard library and easily extensible interpreter stemmed from his frustrations with ABC, which espoused the opposite approach.Rather than building all of its functionality into its core, Python was designed to be highly extensible via modules. This compact modularity has made it particularly popular as a means of adding programmable interfaces to existing applications. Van Rossum\'s vision of a small core language with a large standard library and easily extensible interpreter stemmed from his frustrations with ABC, which espoused the opposite approach.Rather than building all of its functionality into its core, Python was designed to be highly extensible via modules. This compact modularity has made it particularly popular as a means of adding programmable interfaces to existing applications. Van Rossum\'s vision of a small core language with a large standard library and easily extensible interpreter stemmed from his frustrations with ABC, which espoused the opposite approach.Rather than building all of its functionality into its core, Python was designed to be highly extensible via modules. This compact modularity has made it particularly popular as a means of adding programmable interfaces to existing applications. Van Rossum\'s vision of a small core language with a large standard library and easily extensible interpreter stemmed from his frustrations with ABC, which espoused the opposite approach.',ENCRYPT)
    data = res.encode()
    len2 = len(data)
    print(len2)