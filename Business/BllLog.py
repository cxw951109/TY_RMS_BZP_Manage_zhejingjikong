from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityMedicamentVariety import *
from DataEntity.EntityUser import *
from DataEntity.EntityModule import *
from DataEntity.EntityLog import *
from Lib.Utils import *

import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading


# 功能模块
class BllLog(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    #
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllLog, "_instance"):
    #         with BllLog._instance_lock:
    #             if not hasattr(BllLog, "_instance"):
    #                 BllLog._instance = object.__new__(cls)
    #     return BllLog._instance


    def __init__(self, entityType=EntityLog):
        return super().__init__(entityType)

    # 查询某个时间段的日志数据
    def query_LogData_between_time(self, start_time, end_time):
        self.findList(and_(EntityLog.OperateDate >= start_time,
                                                        EntityLog.OperateDate <= end_time))

    # 获取模糊查询日志数据
    def like_Log_data(self, searchValue):
        return self.findList(or_(EntityLog.OperateUserName.like('%' + searchValue + '%'),
            EntityLog.OperateType.like('%' + searchValue + '%')))
