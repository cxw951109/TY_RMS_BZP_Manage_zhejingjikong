from Lib.SerialPort import SerialPort
from collections import Counter
import time

# 天平收发数据文件


class Balance:

    def __init__(self):
        self.ser = SerialPort('/dev/serial_1', 9600)

    def write(self, data):
        self.ser.Write(data.encode())

    def read(self):
        # 过滤天平串口返回
        data_list = []
        while 1:
            time1 = time.time()
            self.write('#')
            content = bytes.decode(self.ser.Read())
            if content:
                data = content.replace(' ', '')[:6]
                data_list.append(data)
                # 获取列表出现最多的值  结果是一个列表取第0个值 为元组  元组由两个值组成 索引0 为出现最多的值 索引1为次数
                most_common_tuple = Counter(data_list).most_common(1)[0] if Counter(data_list).most_common(1) else None
                print(most_common_tuple, 999999999999)
                if most_common_tuple is not None:
                    if most_common_tuple[1] == 3:
                        if most_common_tuple[0] == '+0.00G':
                            return most_common_tuple[0][:-1]
                        return most_common_tuple[0]
            else:
                return None




if __name__ == '__main__':
    a = Balance()
    a.write('#')
    print(a.read())


