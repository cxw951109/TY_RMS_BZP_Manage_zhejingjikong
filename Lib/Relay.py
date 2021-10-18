# -*- coding: utf-8 -*-
from Lib.SerialPort import *
import datetime
import time
import os
import threading
import binascii

"""
控制第一路开	FE 05 00 00 FF 00 98 35
控制第一路关	FE 05 00 00 00 00 D9 C5
控制第二路开	FE 05 00 01 FF 00 C9 F5
控制第二路关	FE 05 00 01 00 00 88 05
控制第三路开	FE 05 00 02 FF 00 39 F5
控制第三路关	FE 05 00 02 00 00 78 05
控制第四路开	FE 05 00 03 FF 00 68 35
控制第四路关	FE 05 00 03 00 00 29 C5
控制第五路开	FE 05 00 04 FF 00 D9 F4
控制第五路关	FE 05 00 04 00 00 98 04
控制第六路开	FE 05 00 05 FF 00 88 34
控制第六路关	FE 05 00 05 00 00 C9 C4
控制第七路开	FE 05 00 06 FF 00 78 34
控制第七路关	FE 05 00 06 00 00 39 C4
控制第八路开	FE 05 00 07 FF 00 29 F4
控制第八路关	FE 05 00 07 00 00 68 04
控制第九路开	FE 05 00 08 FF 00 19 F7
控制第九路关	FE 05 00 08 00 00 58 07
控制第十路开	FE 05 00 09 FF 00 48 37
控制第十路关	FE 05 00 09 00 00 09 C7
控制第十一路开	FE 05 00 0A FF 00 B8 37
控制第十一路关	FE 05 00 0A 00 00 F9 C7
控制第十二路开	FE 05 00 0B FF 00 E9 F7
控制第十二路关	FE 05 00 0B 00 00 A8 07
控制第十三路开	FE 05 00 0C FF 00 58 36
控制第十三路关	FE 05 00 0C 00 00 19 C6
控制第十四路开	FE 05 00 0D FF 00 09 F6
控制第十四路关	FE 05 00 0D 00 00 48 06
控制第十五路开	FE 05 00 0E FF 00 F9 F6
控制第十五路关	FE 05 00 0E 00 00 B8 06
控制第十六路开	FE 05 00 0F FF 00 A8 36
控制第十六路关	FE 05 00 0F 00 00 E9 C6
控制第十七路开	FE 05 00 10 FF 00 99 F0
控制第十七路关	FE 05 00 10 00 00 D8 00
控制第十八路开	FE 05 00 11 FF 00 C8 30
控制第十八路关	FE 05 00 11 00 00 89 C0
控制第十九路开	FE 05 00 12 FF 00 38 30
控制第十九路关	FE 05 00 12 00 00 79 C0
控制第二十路开	FE 05 00 13 FF 00 69 F0
控制第二十路关	FE 05 00 13 00 00 28 00
控制第二十一路开	FE 05 00 14 FF 00 D8 31
控制第二十一路关	FE 05 00 14 00 00 99 C1
控制第二十二路开	FE 05 00 15 FF 00 89 F1
控制第二十二路关	FE 05 00 15 00 00 C8 01
控制第二十三路开	FE 05 00 16 FF 00 79 F1
控制第二十三路关	FE 05 00 16 00 00 38 01
控制第二十四路开	FE 05 00 17 FF 00 28 31
控制第二十四路关	FE 05 00 17 00 00 69 C1
控制第二十五路开	FE 05 00 18 FF 00 18 32
控制第二十五路关	FE 05 00 18 00 00 59 C2
控制第二十六路开	FE 05 00 19 FF 00 49 F2
控制第二十六路关	FE 05 00 19 00 00 08 02
控制第二十七路开	FE 05 00 1A FF 00 B9 F2
控制第二十七路关	FE 05 00 1A 00 00 F8 02
控制第二十八路开	FE 05 00 1B FF 00 E8 32
控制第二十八路关	FE 05 00 1B 00 00 A9 C2
控制第二十九路开	FE 05 00 1C FF 00 59 F3
控制第二十九路关	FE 05 00 1C 00 00 18 03
控制第三十路开	FE 05 00 1D FF 00 08 33
控制第三十路关	FE 05 00 1D 00 00 49 C3
控制第三十一路开	FE 05 00 1E FF 00 F8 33
控制第三十一路关	FE 05 00 1E 00 00 B9 C3
控制第三十二路开	FE 05 00 1F FF 00 A9 F3
控制第三十二路关	FE 05 00 1F 00 00 E8 03
"""


class Relay(object):
    def __init__(self, com="/dev/ttyUSB0", baudrate=9600):
        self.seria = None
        try:
            self.seria = SerialPort(com, baudrate)
            print("32路继电器初始化成功")
            self.start()
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_lineno)
        self.data = [
            #         开                ,           关              31 锁
            ['', ''],
            ['FE 05 00 00 FF 00 98 35', 'FE 05 00 00 00 00 D9 C5'],  # 1
            ['FE 05 00 01 FF 00 C9 F5', 'FE 05 00 01 00 00 88 05'],  # 2
            ['FE 05 00 02 FF 00 39 F5', 'FE 05 00 02 00 00 78 05'],  # 3
            ['FE 05 00 03 FF 00 68 35', 'FE 05 00 03 00 00 29 C5'],  # 4
            ['FE 05 00 04 FF 00 D9 F4', 'FE 05 00 04 00 00 98 04'],  # 5
            ['FE 05 00 05 FF 00 88 34', 'FE 05 00 05 00 00 C9 C4'],  # 6
            ['FE 05 00 06 FF 00 78 34', 'FE 05 00 06 00 00 39 C4'],  # 7
            ['FE 05 00 07 FF 00 29 F4', 'FE 05 00 07 00 00 68 04'],  # 8
            ['FE 05 00 08 FF 00 19 F7', 'FE 05 00 08 00 00 58 07'],  # 9
            ['FE 05 00 09 FF 00 48 37', 'FE 05 00 09 00 00 09 C7'],  # 10
            ['FE 05 00 0A FF 00 B8 37', 'FE 05 00 0A 00 00 F9 C7'],  # 11
            ['FE 05 00 0B FF 00 E9 F7', 'FE 05 00 0B 00 00 A8 07'],  # 12
            ['FE 05 00 0C FF 00 58 36', 'FE 05 00 0C 00 00 19 C6'],  # 13
            ['FE 05 00 0D FF 00 09 F6', 'FE 05 00 0D 00 00 48 06'],  # 14
            ['FE 05 00 0E FF 00 F9 F6', 'FE 05 00 0E 00 00 B8 06'],  # 15
            ['FE 05 00 0F FF 00 A8 36', 'FE 05 00 0F 00 00 E9 C6'],  # 16
            ['FE 05 00 10 FF 00 99 F0', 'FE 05 00 10 00 00 D8 00'],  # 17
            ['FE 05 00 11 FF 00 C8 30', 'FE 05 00 11 00 00 89 C0'],  # 18
            ['FE 05 00 12 FF 00 38 30', 'FE 05 00 12 00 00 79 C0'],  # 19
            ['FE 05 00 13 FF 00 69 F0', 'FE 05 00 13 00 00 28 00'],  # 20
            ['FE 05 00 14 FF 00 D8 31', 'FE 05 00 14 00 00 99 C1'],  # 21
            ['FE 05 00 15 FF 00 89 F1', 'FE 05 00 15 00 00 C8 01'],  # 22
            ['FE 05 00 16 FF 00 79 F1', 'FE 05 00 16 00 00 38 01'],  # 23
            ['FE 05 00 17 FF 00 28 31', 'FE 05 00 17 00 00 69 C1'],  # 24
            ['FE 05 00 18 FF 00 18 32', 'FE 05 00 18 00 00 59 C2'],  # 25
            ['FE 05 00 19 FF 00 49 F2', 'FE 05 00 19 00 00 08 02'],  # 26
            ['FE 05 00 1A FF 00 B9 F2', 'FE 05 00 1A 00 00 F8 02'],  # 27
            ['FE 05 00 1B FF 00 E8 32', 'FE 05 00 1B 00 00 A9 C2'],  # 28
            ['FE 05 00 1C FF 00 59 F3', 'FE 05 00 1C 00 00 18 03'],  # 29
            ['FE 05 00 1D FF 00 08 33', 'FE 05 00 1D 00 00 49 C3'],  # 30
            ['FE 05 00 1E FF 00 F8 33', 'FE 05 00 1E 00 00 B9 C3'],  # 31
            ['FE 05 00 1F FF 00 A9 F3', 'FE 05 00 1F 00 00 E8 03']  # 32
        ]

    def control_switch(self, num, switch):
        if str(switch) == '1':  # 开
            cmd = self.data[int(num)][0]
        else:  # 关
            cmd = self.data[int(num)][1]
        print(cmd)
        self.seria.Write(bytes.fromhex(cmd))
        time.sleep(0.2)
        val = str(binascii.b2a_hex(self.seria.Read()).decode())
        if val:
            return 'ok'
        else:
            return '应答有误'

    def start(self):
        p1 = threading.Thread(target=self.getStatus)
        p1.start()

    def getStatus(self):
        while True:
            self.seria.Write(bytes.fromhex('FE 02 00 00 00 01 AD C5'))
            time.sleep(0.1)
            val = str(binascii.b2a_hex(self.seria.Read()).decode())
            print(val)
            if(val=='fe020101505c'.lower()):
                self.seria.Write(bytes.fromhex('FE 0F 00 00 00 20 04 00 00 00 00 F7 9F'))
                time.sleep(0.1)
                self.seria.Read()
            time.sleep(0.6)



if __name__ == '__main__':
    a = Relay()
