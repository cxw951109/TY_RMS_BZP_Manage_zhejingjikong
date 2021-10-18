from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#温湿度记录实体类
class EntityHumitureRecord(declarative_base()):
    __tablename__ = "RMS_HumitureRecord"

    RecordId = Column(String(50),primary_key=True) #记录ID
    DeviceId = Column(String(50)) #设备ID
    ClientId = Column(String(50)) #终端ID
    ClientName = Column(String(50)) #终端名称
    CustomerId = Column(String(50)) #客户ID
    Temperature = Column(Float) #温度值
    Humidity = Column(Float) #湿度值
    RecordDate = Column(String(50)) #记录日期
    IsAdd = Column(Integer)