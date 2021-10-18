from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityPurchaseOrder import *
from DataEntity.EntityPurchaseOrderDetailed import *
from Lib.Utils import *
from Lib.Model import *

import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading

class BllPurchaseOrder(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    #
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllLog, "_instance"):
    #         with BllLog._instance_lock:
    #             if not hasattr(BllLog, "_instance"):
    #                 BllLog._instance = object.__new__(cls)
    #     return BllLog._instance


    def __init__(self, entityType=EntityPurchaseOrder):
        return super().__init__(entityType)

    # 获取采购单数据
    def getPurchaseOrderList(self,pageParam,PurchaseOrderCode='',CreateUserName='',PurchaseOrderDrugInfo='',PurchaseOrderStatus=''):
        orm_query= self.findList().order_by(desc(EntityPurchaseOrder.CreateDate))
        if(PurchaseOrderCode):
            orm_query= orm_query.filter(EntityPurchaseOrder.PurchaseOrderCode.like('%'+PurchaseOrderCode+'%'))
        if(CreateUserName):
            orm_query= orm_query.filter(EntityPurchaseOrder.CreateUserName.like('%'+CreateUserName+'%'))
        if(PurchaseOrderDrugInfo):
            orm_query= orm_query.filter(EntityPurchaseOrder.PurchaseOrderDrugInfo.like('%'+PurchaseOrderDrugInfo+'%'))
        if(PurchaseOrderStatus):
            orm_query= orm_query.filter(EntityPurchaseOrder.PurchaseOrderStatus==int(PurchaseOrderStatus))
        orm_query.order_by(desc(EntityPurchaseOrder.CreateDate))
        return self.queryPage(orm_query,pageParam)

    # 获取等待采购数据
    def getWaitingPurchaseList(self,pageParam,PurchaseOrderCode='',CreateUserName='',PurchaseOrderDrugInfo=''):
        orm_query= self.findList(and_(EntityPurchaseOrder.PurchaseOrderStatus==3,EntityPurchaseOrder.IsCompletePurchase!=1)).order_by(desc(EntityPurchaseOrder.CreateDate))
        if(PurchaseOrderCode):
            orm_query= orm_query.filter(EntityPurchaseOrder.PurchaseOrderCode.like('%'+PurchaseOrderCode+'%'))
        if(CreateUserName):
            orm_query= orm_query.filter(EntityPurchaseOrder.CreateUserName.like('%'+CreateUserName+'%'))
        if(PurchaseOrderDrugInfo):
            orm_query= orm_query.filter(EntityPurchaseOrder.PurchaseOrderDrugInfo.like('%'+PurchaseOrderDrugInfo+'%'))
        return self.queryPage(orm_query,pageParam)

    # 获取完成采购数据
    def getCompletePurchaseList(self,pageParam,PurchaseOrderCode='',CreateUserName='',PurchaseOrderDrugInfo=''):
        orm_query= self.findList(EntityPurchaseOrder.IsCompletePurchase==1).order_by(desc(EntityPurchaseOrder.CreateDate))
        if(PurchaseOrderCode):
            orm_query= orm_query.filter(EntityPurchaseOrder.PurchaseOrderCode.like('%'+PurchaseOrderCode+'%'))
        if(CreateUserName):
            orm_query= orm_query.filter(EntityPurchaseOrder.CreateUserName.like('%'+CreateUserName+'%'))
        if(PurchaseOrderDrugInfo):
            orm_query= orm_query.filter(EntityPurchaseOrder.PurchaseOrderDrugInfo.like('%'+PurchaseOrderDrugInfo+'%'))
        return self.queryPage(orm_query,pageParam)
