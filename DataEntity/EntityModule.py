from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#终端模块实体类
class EntityModule(declarative_base()):
    __tablename__ = "RMS_Module"

    ModuleId = Column(String(50),primary_key=True) #模块ID
    ModuleType = Column(String(50)) #模块类型
    ModuleCode = Column(String(50)) #模块编号
    ModuleName = Column(String(50)) #模块名称
    Icon = Column(String(50)) #图标路径
    UrlAddress = Column(String(50)) #url地址
    SortIndex = Column(Integer) #排序序号
    ModuleWeight = Column(Integer) #模块权重
    ParentId = Column(String(50)) #父级ID
    IsEnabled = Column(Integer) #是否启用
    Description = Column(String(50)) #备注
    CreateDate = Column(String(50)) #创建日期
    CreateUserId = Column(String(50)) #创建用户ID
    CreateUserName = Column(String(50)) #创建用户名
    IsAdd = Column(Integer)