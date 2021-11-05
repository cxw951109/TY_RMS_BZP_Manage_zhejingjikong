import time
import serial
from time import sleep
class SerialPort(object):
    def __init__(self,Name,BaudRate):
        self.ser = serial.Serial(Name, BaudRate, timeout=0.1)

    def Read(self,num=0):
        data=None
        while True:
            count = self.ser.inWaiting() #获取接收缓存区的字节数
            if(num==0):
                data = self.ser.readall()
            else:
                data = self.ser.read(count)
            if data == None:
                continue
            else:
                break
        return data

    def Write(self,data):
        self.ser.write(data)

    def close(self):
        self.ser.close()

if __name__ == "__main__":
    sp = SerialPort('COM9', 9600)
    value = sp.Write(b'#')
    print(bytes.decode(sp.Read()))






