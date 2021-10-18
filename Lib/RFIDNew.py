# -*- coding: utf-8 -*-
from Lib.SerialPort import *
import datetime
import time
import os
import threading
import binascii


class RFIDNew(object):
    def __init__(self, com="/dev/ttyUSB1", baudrate=115200):
        self.seria = None
        try:
            self.seria = SerialPort(com, baudrate)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_lineno)

    def open(self):
        self.seria.Write(bytes.fromhex('7E5509000001004000004222'))
        time.sleep(0.3)
        self.seria.Read()
        time.sleep(0.3)

    def get_stay_label(self):
        self.open()
        self.seria.Write(bytes.fromhex('7E 55 08 00 00 01 00 41 00 99 11'))
        time.sleep(0.2)
        val = str(binascii.b2a_hex(self.seria.Read()).decode())
        print('datetime:', datetime.datetime.now())
        print(val)
        if val.startswith('7e5500010000001f4100f1001e'):
            data = val[26:]
            index_start = 0
            index_end = 16
            list01 = []
            weizhi = 1
            # list02 = []
            list03 = []
            for i in range(int(len(data) // 16)):
                if int(data[index_start:index_end], 16) != 0:
                    list01.append(data[index_start:index_end])
                    # list02.append(weizhi)
                    x = int(weizhi % 5)
                    if x == 0:
                        x = 5
                    str_zb = str(x) + '_' + str(6 - ((weizhi - 1) // 5))
                    list03.append(str_zb)
                weizhi += 1
                index_start += 16
                index_end += 16
            # print(list01)
            # print(list02)
            # print(list03)
            return [list01, list03]
            # print(len('7e5500010000001f4100f1001e'))
        else:
            return ''


if __name__ == '__main__':
    a = RFIDNew()
    a.get_stay_label()
