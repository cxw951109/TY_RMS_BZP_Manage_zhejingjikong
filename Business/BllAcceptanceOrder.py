from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityAcceptanceOrder import *
from DataEntity.EntityAcceptanceOrderDetailed import *
from Lib.Utils import *

import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading

class BllAcceptanceOrder(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    #
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllLog, "_instance"):
    #         with BllLog._instance_lock:
    #             if not hasattr(BllLog, "_instance"):
    #                 BllLog._instance = object.__new__(cls)
    #     return BllLog._instance


    def __init__(self, entityType=EntityAcceptanceOrder):
        return super().__init__(entityType)

    # 获取验收单数据
    def getAcceptanceOrderList(self,pageParam,AcceptanceOrderCode='',CreateUserName='',AcceptanceOrderDrugInfo='',AcceptanceOrderStatus=''):
        orm_query= self.findList().order_by(desc(EntityAcceptanceOrder.CreateDate))
        if(AcceptanceOrderCode):
            orm_query= orm_query.filter(EntityAcceptanceOrder.AcceptanceOrderCode.like('%'+AcceptanceOrderCode+'%'))
        if(CreateUserName):
            orm_query= orm_query.filter(EntityAcceptanceOrder.CreateUserName.like('%'+CreateUserName+'%'))
        if(AcceptanceOrderDrugInfo):
            orm_query= orm_query.filter(EntityAcceptanceOrder.AcceptanceOrderDrugInfo.like('%'+AcceptanceOrderDrugInfo+'%'))
        if(AcceptanceOrderStatus):
            orm_query= orm_query.filter(EntityAcceptanceOrder.AcceptanceOrderStatus==int(AcceptanceOrderStatus))
        return self.queryPage(orm_query,pageParam)

