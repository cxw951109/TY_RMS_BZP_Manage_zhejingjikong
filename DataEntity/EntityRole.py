from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#用户角色实体类
class EntityRole(declarative_base()):
    __tablename__ = "RMS_Role"

    RoleId = Column(String(50),primary_key=True) #角色ID
    RoleCode = Column(String(50)) #角色编号
    RoleName = Column(String(50)) #角色名
    RoleLevel = Column(Integer) #角色级别
    SortIndex = Column(Integer) #排序序号
    IsEnabled = Column(Integer) #是否启用
    Description = Column(String(50)) #备注
    IsAdd = Column(Integer)
