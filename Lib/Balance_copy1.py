from Lib.SerialPort import SerialPort
from collections import Counter
import time

# 天平收发数据文件


class Balance:

    def __init__(self):
        self.ser = SerialPort('COM3', 9600)

    def write(self, data):
        self.ser.Write(data.encode())

    def read(self):
        # 数据稳定之后返回值 同一个值出现3次返回
        stable_list = []

        while 1:
            self.write('IP\r\n')
                
            content = bytes.decode(self.ser.Read())
            if content:
                if content[0] != 'E':
                    # 分割获取到的数据
                    content = content.split(' ')
                    # 遍历列表如果有值则return
                    for val in content:
                        if val:
                            stable_list.append(val)
                            break
                    return_val = Counter(stable_list).most_common(1)[0]
                    print(return_val)
                    print(stable_list)
                    if return_val[1] == 3:
                        return return_val[0]

                elif content[0] == 'E':
                    return '关机'

                else:
                    return None
            else:
                return None

if __name__ == '__main__':
    a = Balance()
    a.write('IP\r\n')
    print(a.read())


