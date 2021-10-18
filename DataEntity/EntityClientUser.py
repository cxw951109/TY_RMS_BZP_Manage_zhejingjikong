from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#用户终端权限实体类
class EntityClientUser(declarative_base()):
    __tablename__ = "RMS_ClientUser"
    ClientUserId = Column(String(50),primary_key=True)  # 用户ID
    ClientId = Column(String(50)) #终端ID
    UserId = Column(String(50)) #用户ID


