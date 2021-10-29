import socket
import re
import time
import threading
from  Business.BllMedicament import *

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
    server.listen(30)
    socketList=[]
    acceptClientFlag=False
    monitorLockFlag=True
    Data={"terminal":"","mes":""}
    # deviceSetList={
    #     '127.0.0.1':'1号终端',
    #     '192.168.10.175':'2号终端'
    # }
    deviceSetList=['1号终端','2号终端','3号终端']

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
                print(sock,addr)
                sock.settimeout(10)
                # terminal = cls.deviceSetList[addr[0]]
                cls.socketList.append(sock)
                threading.Thread(target=cls.monitorLockFun).start()
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
    def clear_data(cls):
        """
        清空变量
        """
        cls.Data = {"terminal":"","mes":""}

    @classmethod
    def get_data(cls,data,clientId,clientSock):
        """
        接收数据入库
        """
        # data_list =[]
        for i in data:
            barcode =str(i["rfid"])
            index =i["index"]+1
            # data_list.append(str(index))
            data_list2= []
            if barcode =='00000000':
                medicament_obj = BllMedicament().findEntity(and_(EntityMedicament.ClientId ==clientId,EntityMedicament.Place == index))
                if medicament_obj:
                    medicament_obj.Place = ''
                    BllMedicament().update(medicament_obj)
                    data_list2.append(str(index))
            else:
                medicament_obj = BllMedicament().findEntity(and_(EntityMedicament.ClientId ==clientId,EntityMedicament.BarCode == barcode))
                if medicament_obj:
                    medicament_obj.Place = index
                    BllMedicament().update(medicament_obj)
                    data_list2.append(str(index))
        if data_list2:
            clientSock.send(('lightoff'+"~".join(data_list2)).encode())
            print('灭灯:','lightoff'+"~".join(data_list2))


    @classmethod
    def monitorLockFun(cls):
        """
        监听用户
        """
        while cls.monitorLockFlag:
            num =0
            for clientSock in cls.socketList:
                num =num+1
                last_result = []
                # terminal =cls.deviceSetList[clientSock.getsockname()[0]]
                terminal = cls.deviceSetList[num-1]
                client_obj = BllClient().findEntity(EntityClient.ClientName == terminal)
                if client_obj:
                    clientId =client_obj.ClientId
                    try:
                        if cls.Data["terminal"]== terminal and cls.Data["mes"] !="clockopen":
                            print(terminal, "开锁")
                            clientSock.send(cls.Data["mes"].encode())
                            cls.clear_data()
                        clientSock.send('dooropen'.encode())
                        door_status =clientSock.recv(cls.BUFSIZ)#获取门状态1开门0关门
                        print("获取"+terminal+"门状态:",door_status.decode())
                        if door_status.decode() =='1':
                            clientSock.send('getrfiddata'.encode())
                            result_data=clientSock.recv(cls.BUFSIZ)
                            result_data1 =re.findall('.{8}',result_data.decode())
                            if last_result !=[]:
                                diff =[{"index":i,"rfid":result_data1[i]} for i in range(len(result_data1)) if result_data1[i] != last_result[i]]
                            else:
                                diff =[{"index":i,"rfid":result_data1[i]} for i in range(len(result_data1))]
                            print("RFID diff:",diff)
                            if diff:
                                cls.get_data(diff,clientId,clientSock)
                            #与上次结果对比,RMS_Medicament入库
                            last_result =result_data1
                        else:
                            if cls.Data["terminal"] == terminal and cls.Data["mes"] == "clockopen":
                                print(terminal,"开锁")
                                clientSock.send("clockopen".encode())
                                cls.clear_data()
                    except Exception as e:
                        # print('监听' + terminal + '错误:', str(e))
                        if e.errno == 10053 or e.errno ==10038:
                            cls.socketList.remove(clientSock)
                            break


AccuLockTcpServer().startAcceptClient()



