from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#柜子抽屉权限实体类
class EntityClientCellUser(declarative_base()):
    __tablename__ = "RMS_ClientCellUser"

    Id = Column(String(50),primary_key=True) #ID
    ClientCellId = Column(String(50)) #抽屉ID
    ClientCellCode = Column(String(50)) #抽屉编号
    ClientId = Column(String(50)) #终端ID
    ClientCode = Column(String(50)) #终端编号
    UserId = Column(String(50)) #用户ID
