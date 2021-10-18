from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityApproveInfo import *
from DataEntity.EntityApproveInfoProcess import *
from Lib.Utils import *

import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading

class BllApproveInfoProcess(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    #
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllLog, "_instance"):
    #         with BllLog._instance_lock:
    #             if not hasattr(BllLog, "_instance"):
    #                 BllLog._instance = object.__new__(cls)
    #     return BllLog._instance


    def __init__(self, entityType=EntityApproveInfoProcess):
        return super().__init__(entityType)

    # 获取类型审批流程
    def getApproveInfoProcess(self, infoId):
        return self.findList(EntityApproveInfoProcess.ApproveInfoId==infoId).order_by(desc(EntityApproveInfoProcess.SortIndex)).all()

