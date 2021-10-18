from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#终端模块权限实体类
class EntityModuleRelation(declarative_base()):
    __tablename__ = "RMS_ModuleRelation"

    ModuleRelationId = Column(String(50),primary_key=True) #关系ID
    CustomerId = Column(String(50)) #客户ID
    ObjectType = Column(String(50)) #对象类型（1：角色 2：用户）
    ObjectId = Column(String(50)) #对象ID
    ModuleType = Column(String(50)) #模块类型
    ModuleId = Column(String(50)) #模块ID
    CreateDate = Column(String(50)) #创建日期
    CreateUserId = Column(String(50)) #创建用户ID
    CreateUserName = Column(String(50)) #创建用户名
    IsAdd = Column(Integer)

