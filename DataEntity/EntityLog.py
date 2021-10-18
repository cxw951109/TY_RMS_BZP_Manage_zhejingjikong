from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#日志信息实体类
class EntityLog(declarative_base()):
    __tablename__ = "RMS_Log"

    LogId = Column(String(50),primary_key=True) #日志ID
    CustomerId = Column(String(50)) #客户ID
    LogType = Column(String(50)) #日志类型
    OperateUserId = Column(String(50)) #操作用户ID
    OperateAccount = Column(String(50)) #操作账户
    OperateUserName = Column(String(50)) #操作用户名
    OperateTypeCode = Column(String(50)) #操作类型编号
    OperateType = Column(String(50)) #操作类型
    IPAddress = Column(String(50)) #IP地址
    ExecuteResultCode = Column(String(50)) #执行结果代码
    ExecuteResult = Column(String(50)) #执行结果
    OperateDate = Column(String(50)) #操作日期
    IsAdd = Column(Integer)