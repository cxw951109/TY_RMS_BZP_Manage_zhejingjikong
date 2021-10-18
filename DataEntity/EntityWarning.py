from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#预警信息实体类
class EntityWarning(declarative_base()):
    __tablename__ = "RMS_Warning"

    WarningId = Column(String(50),primary_key=True) # 预警ID
    CustomerId = Column(String(50)) # 客户ID
    ObjectType = Column(String(50)) # 预警对象类型
    ObjectId = Column(String(50)) # 预警对象
    ObjectName = Column(String(50)) # 对象名称
    WarningContent = Column(String(50)) # 预警内容
    WarningDate = Column(String(50)) # 预警日期
    WarningUserId = Column(String(50)) # 预警用户ID
    WarningUserName = Column(String(50)) # 预警用户名
    IsSolve = Column(Integer) # 是否解决
    SolveUserId = Column(String(50)) # 解决用户ID
    SolveUserName = Column(String(50)) # 解决用户名
    SolveDate = Column(String(50)) # 解决日期
    SolveContent = Column(Text) # 解决内容
    IsAdd = Column(Integer)