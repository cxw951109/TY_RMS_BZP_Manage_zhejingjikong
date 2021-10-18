from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityPeriodCheck import *
from DataEntity.EntityPeriodCheckDetailed import *
from Lib.Utils import *
from Lib.Model import *

import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading

class BllPeriodCheckDetailed(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    #
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllLog, "_instance"):
    #         with BllLog._instance_lock:
    #             if not hasattr(BllLog, "_instance"):
    #                 BllLog._instance = object.__new__(cls)
    #     return BllLog._instance


    def __init__(self, entityType=EntityPeriodCheckDetailed):
        return super().__init__(entityType)

    # 获取期间核查数据列表
    def getPeriodCheckDetailedList(self,pageParam,periodCheckId):
        orm_query= self.findList(EntityPeriodCheckDetailed.PeriodCheckId==periodCheckId).order_by(desc(EntityPeriodCheckDetailed.CreateDate))
        return self.queryPage(orm_query,pageParam)

    # 获取期间核查数据列表
    def getPeriodCheckDetailedListByDrugId(self,DrugId):
        return self.findList(EntityPeriodCheckDetailed.DrugId==DrugId).order_by(desc(EntityPeriodCheckDetailed.CreateDate)).all()
