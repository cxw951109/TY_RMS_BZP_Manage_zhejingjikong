import socket
from time import ctime
import binascii
import re
import threading
from Business.BllUser import *
from Business.BllLog import *
from DataEntity.EntityUser import *
from DataEntity.EntityLog import *
from Lib.Utils import *

class AccuLockTcpServer:
    """
    Acculock锁监听控制服务
    """
    def __init__(self):
        super().__init__()

    BUFSIZ = 1024
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind(('127.0.0.1', 9527))
    server.listen(5)
    acceptClientFlag=False
    monitorLockFlag=True
    Data={"terminal":"JY-163","mes":"lighton1~3~5"}
    deviceSetList={
        '127.0.0.1':'JY-163',
    }

    @classmethod
    def startAcceptClient(cls):
        """
        开始监听客户端加入
        """
        cls.acceptClientFlag=True
        acceptClientThread=threading.Thread(target=cls.acceptClientFun)
        acceptClientThread.start()

    @classmethod
    def stopAcceptClient(cls):
        """
        停止监听客户端加入
        """
        cls.acceptClientFlag=False

    @classmethod
    def acceptClientFun(cls):
        """
        监听客户端加入处理
        """
        while cls.acceptClientFlag:
            try:
                sock, addr = cls.server.accept()
                sock.settimeout(10)
                terminal = cls.deviceSetList[addr[0]]
                threading.Thread(target=cls.monitorLockFun(sock,terminal)).start()
            except Exception as e:
                print('监听客户端加入错误:',str(e))


    @classmethod
    def startMonitorLock(cls):
        """
        开始监听
        """
        cls.monitorLockFlag=True

    @classmethod
    def stopMonitorLock(cls):
        """
        停止监听
        """
        cls.monitorLockFlag=False

    @classmethod
    def monitorLockFun(cls,clientSock,terminal):
        """
        监听用户
        """
        print(terminal, clientSock)
        last_result = []
        while cls.monitorLockFlag:
            try:
                if cls.Data["terminal"]== terminal:
                    clientSock.send(cls.Data["mes"].encode())
                    cls.Data = {"terminal":"","mes":""}
                clientSock.send('dooropen'.encode())
                door_status =clientSock.recv(cls.BUFSIZ)#获取门状态1开门0关门
                print(door_status.decode())
                if door_status.decode() =='1':
                    clientSock.send('getrfiddata'.encode())
                    result_data=clientSock.recv(cls.BUFSIZ)
                    result_data1 =re.findall('.{8}',result_data.decode())
                    if last_result !=[]:
                        diff =[{"index":i,"rfid":result_data1[i]} for i in range(len(result_data1)) if result_data1[i] != last_result[i]]
                    else:
                        diff =[{"index":i,"rfid":result_data1[i]} for i in range(len(result_data1))]
                    print(diff)
                    #与上次结果对比,RMS_Medicament入库位置
                    last_result =result_data1
                time.sleep(1)
            except Exception as e:
                print('监听用户错误:',str(e))
                if e.errno == 10053 or e.errno ==10038:
                    break


AccuLockTcpServer().startAcceptClient()



