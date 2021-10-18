from Lib.SerialPort import *
from Lib.Utils import *
import datetime
import time
import os
import threading
import binascii


class RFIDDevice(object):
    def __init__(self):
        self.seria = SerialPort("/dev/ttyS0",19200)


    # 获取rfid标签值
    def getRFID(self):

        print('进入请求、、、')
        self.seria.Write(bytes.fromhex('10 FF 4D'))
        val = str(binascii.b2a_hex(self.seria.Read()).decode())
        print(val)
        if(val.startswith('10ff08')):
            return val[6:]
        else:
            return ''

