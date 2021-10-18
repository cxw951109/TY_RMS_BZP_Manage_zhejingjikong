from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#终端版本实体类
class EntityClientVersion(declarative_base()):
    __tablename__ = "RMS_ClientVersion"

    VersionId = Column(String(50),primary_key=True) #版本ID
    VersionName = Column(String(50)) #版本名称
    VersionCode = Column(String(50)) #版本编号
    DownLink = Column(String(50)) #下载链接
    VersionInfo = Column(String(50)) #版本信息
    CreateDate = Column(String(50)) #创建时间
    CreateUserId = Column(Integer) #创建用户ID
    CreateUserName = Column(String(50)) #创建用户名
    IsAdd = Column(Integer)
