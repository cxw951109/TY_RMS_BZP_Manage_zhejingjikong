from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#终端实体类
class EntityClient(declarative_base()):
    __tablename__ = "RMS_Client"

    ClientId = Column(String(50),primary_key=True) #终端ID
    ClientCode = Column(String(50)) #终端编号
    ClientName = Column(String(50)) #终端名称
    CustomerId = Column(String(50)) #客户ID
    ClientType = Column(String(50)) #客户类型
    ClientTitle = Column(String(50)) #终端标题
    ClientUseCode = Column(String(50)) #终端编码
    Place = Column(String(50)) #位置
    IPaddress = Column(String(50)) #IP地址
    ContactPeopleName = Column(String(50)) #联系人电话
    ContactPhone = Column(String(50)) #联系人
    TotalRunTime = Column(Integer) #总运行时长
    TemperatureSetValue = Column(Float) #温度设定控温值
    TemperatureMaxValue = Column(Float) #温度预警上限
    TemperatureMinValue = Column(Float) #温度预警下限
    HumidityMaxValue = Column(Float) #湿度预警上限
    HumidityMinValue = Column(Float) #湿度预警下限
    FilterProductionDate = Column(String(50)) # 滤芯生产日期
    FilterShelfLife = Column(Integer) #滤芯保质期
    FilterShelfLifeWarningValue = Column(Integer) #滤芯保质期到期提前预警天数
    IsEnabled = Column(Integer) #是否启用
    SortIndex = Column(Integer) #排序序号
    ParentId = Column(Integer) #父级ID
    Description = Column(String(200)) #备注
    IsAdd = Column(Integer)


