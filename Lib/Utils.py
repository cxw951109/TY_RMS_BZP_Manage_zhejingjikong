import hashlib
import uuid
import json
import datetime
import time
import hashlib
import os
import platform
import psutil
import random
import functools
import logging
import logging.config
from dateutil import relativedelta, parser

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from Lib.AlchemyJsonEncoder import *
from Business.BllClient import *
from Business.BllHumitureRecord import *

from DataEntity.EntityHumitureRecord import *
# 判断当前系统是linux还是windows
system_name = platform.system()
try:
    # 加载settings里面的配置项
    logging.config.dictConfig(settings.LOGGING)
    logger = logging.getLogger('default')
except:
    pass


"""通用工具类"""
class Utils(object):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    #MD5加密
    def MD5(str):
        # 创建md5对象
        hl = hashlib.md5()
        hl.update(str.encode(encoding='utf-8'))
        return hl.hexdigest()

    #获取唯一识别码
    @staticmethod
    def UUID():
        return str(uuid.uuid1())

    @staticmethod
    def getMacAddress():
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0,11,2)])

    #将sqlAlchemy Sql执行数据对象列表转换为实体列表
    @staticmethod
    def mysqlTable2Model(dataList):
        return [dict(zip(result.keys(), [ (x if x is not None else '') for x in result.values() ]  )) for result in dataList]

    #生成统一格式接口数据
    @staticmethod
    def resultData(status,message,data=""):
        return {"status":status,"message":message,"data":data}
    #生成统一格式接口数据
    @staticmethod
    def resultAlchemyData(data):
        return json.dumps(data, cls=AlchemyEncoder)

    #按时间生成随机文件名
    @staticmethod
    def getFileName():
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")#生成当前的时间
        randomNum = random.randint(0,100)#生成随机数n,其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

    #按时间生成随机订单号
    @staticmethod
    def createOrderCode():
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]#生成当前的时间
        randomNum = random.randint(0,100)#生成随机数n,其中0<=n<=100
        uniqueNum = str(nowTime)
        return uniqueNum

    #创建文件夹
    def mkdir(path):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)

    # 随机生成一段sha256加密
    @staticmethod
    def sha256_secret():
        sha256 = hashlib.sha256()
        sha256.update(str(random.random()).encode('utf-8'))
        res = sha256.hexdigest()
        return res


    # 读取redis缓存装饰器
    @staticmethod
    def redis_cache(key, timeout):
        def _redis_cache(func):
            def warpper(*args, **kwargs):
                # 判断缓存是否存在
                if cache.has_key(key):
                    print('get cache')
                    data = cache.get(key)
                else:
                    print('没有获取到缓存')
                    data = func(*args, **kwargs)
                    cache.set(key, json.loads(Utils.resultAlchemyData(data)), timeout)
                return data

            return warpper

        return _redis_cache

    # 获取最近24小时的值
    def get_24_hours(self):
        # 获取当前的小时值
        data_hour_list = []
        curtime_hour = datetime.datetime.now().strftime('%H')
        y = int(curtime_hour)
        for x in range(24):
            data_hour_list.append(str(y) + ':00')
            if y == 0:
                y = 23
                continue
            y -= 1

        return data_hour_list



    #  获取温湿度的数据
    def get_temperature_or_humidity(self, params=None):

        # params 传参则代表湿度, 不传参就代表温度
        # 前段echarts展示series 字段的所有数据
        series_list = []
        # 获取最近24小时的值
        data_hour_list =list(reversed(self.get_24_hours()))
        # 获取所有客户端
        client_list = BllClient().getAllClientList()
        # 客户端名字列表
        client_name_list = []

        for client_obj in client_list:
            client_name_list.append(client_obj.ClientName)
            # 定义两个字典, 键相同, 一个字典保存次数, 一个字典保存温度总数
            temperature_dict = {}
            temperature_dict_count = {}
            # 获取当前时间
            curtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 当前时间减去24小时
            start_time = (parser.parse(datetime.datetime.now().strftime('%Y-%m-%d %H')) + relativedelta.relativedelta(hours=-23)).strftime('%Y-%m-%d %H:%M:%S')

            # 获取温湿度的所有对象
            humiture_obj_list = BllHumitureRecord().findList(and_(EntityHumitureRecord.ClientId == client_obj.ClientId,
                                                                  EntityHumitureRecord.RecordDate.between(start_time,
                                                                                                          curtime))).all()

            # 遍历求出每一个对象
            for humiture_obj in humiture_obj_list:

                # 获取每一个对象的RecordDate的时间值
                hum_hour = humiture_obj.RecordDate.strftime('%H')
                # 判断当前hum_hour是否在定义的字典中, 如果没有,hum_hour作为键
                # 1作为当前时间共有几个数值, humiture_obj.Temperature的温度作为值
                if hum_hour not in temperature_dict:
                    temperature_dict_count[hum_hour] = 1
                    if params:
                        temperature_dict[hum_hour] = humiture_obj.Humidity
                    else:
                        temperature_dict[hum_hour] = humiture_obj.Temperature
                # 如果存在, 数值+1, 温度值叠加
                else:
                    if params:
                        temperature_dict[hum_hour] += humiture_obj.Humidity
                    else:
                        temperature_dict[hum_hour] += humiture_obj.Temperature
                    temperature_dict_count[hum_hour] += 1

            # 求温度的平均值
            for each_count in temperature_dict_count.keys():
                if each_count in temperature_dict:
                    temperature_dict[each_count] = round(temperature_dict[each_count]
                                                         / temperature_dict_count[each_count], 2)
            # 求出当前时间近24小时的温度值和小时值
            data_temperate = []
            for data_hour in data_hour_list:
                if len(data_hour) == 4:
                    data_hour = '0' +  str(data_hour)

                if str(data_hour[:-3]) in temperature_dict:
                    data_temperate.append(temperature_dict[data_hour[:-3]])
                else:
                    data_temperate.append('0.0')

            series_list.append({"name": client_obj.ClientName, "type": "line",
                                "data": data_temperate,

                                "markPoint":
                                    {"data": [{"type": "max", "name": "最大值"}, {"type": "min", "name": "最小值"}]},
                                "markLine": {"data": [{"type": "average", "name": "平均值"}]}})

        data = {"title": {"text": "最近24小时温度变化"},
                "tooltip": {"trigger": "axis"},
                # 下载为图片
                'toolbox': {
                    'show': 'true',
                    'feature': {
                        'saveAsImage': {
                            'show': 'true',
                            'type': 'jpeg',
                            'name': '温湿度监控折线图',
                            'excludeComponents': "['toolbox']",
                            'pixelRatio': '2',
                            'icon': 'image:///static/img/download.png/'
                        },
                        'magicType': {'show': 'true', 'type': ['line', 'bar']},
                        'restore': {
                           'show': 'true',
                        }
                    }

                },
                "legend": {"data": client_name_list},
                "grid": {"x": 55, "x2": 55, "y2": 24},
                "calculable": True,
                "xAxis": [{"type": "category",
                           "boundaryGap": False,
                           "data": data_hour_list}],
                "yAxis": [{"type": "value", "axisLabel": {"formatter": "{value} °C"}}],
                "series": series_list}

        return data

    @staticmethod
    def log_exception(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                return func(*args, **kwargs)
            except Exception as e:

                logger.exception("[Error in {}] msg: {}".format(__name__, str(e)))
                raise

        return wrapper

    # # 获取当前用户桌面路径  import winreg
    # @staticmethod
    # def get_desktop():
    #     key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    #                          r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    #     return winreg.QueryValueEx(key, "Desktop")[0]

    @staticmethod
    def get_user_ip(request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            return request.META['HTTP_X_FORWARDED_FOR']
        else:
            return request.META['REMOTE_ADDR']


    # 发送邮件
    @staticmethod
    def send_email(email):
        from django.core.mail import EmailMultiAlternatives

        subject = '来自www.1117.link的注册确认邮件'

        text_content = '''欢迎注册www.1117.link，这里是大鱼的论坛站点，专注于Python和Django技术的分享！\
                            如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

        html_content = '''
                            <p>感谢注册 target=blank>www.1117.link</a>，\
                            这里是大鱼的博客和教程站点，专注于Python和Django技术的分享！</p>
                            <p>请点击站点链接完成注册确认！</p>
                            <p>此链接有效期为{}天！</p>
                            '''.format('127.0.0.1:80', settings.CONFIRM_DAYS)
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    #获取当前插入U盘路径
    @staticmethod
    def getUDiskPath():
        if system_name == 'Windows':
            disk_list = psutil.disk_partitions()
            # 获取U盘路径
            u_path = [disk.device for disk in disk_list if disk.opts == 'rw,removable']
            if u_path:
                return u_path[0]
        elif system_name == 'Linux':
            import pyudev
            context = pyudev.Context()
            removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
            for device in removable:
              partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
              #print("All removable partitions: {}".format(",
              #".join(partitions)))
              #print("Mounted removable partitions:")
              for p in psutil.disk_partitions():
                  if p.device in partitions:
                      return p.mountpoint
        return ""



