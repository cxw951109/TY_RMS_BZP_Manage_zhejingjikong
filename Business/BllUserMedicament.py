from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityUserMedicament import *
from Lib.Utils import *
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading


#用户试剂业务逻辑类
class BllUserMedicament(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllUserMedicament, "_instance"):
    #         with BllUserMedicament._instance_lock:
    #             if not hasattr(BllUserMedicament, "_instance"):
    #                 BllUserMedicament._instance = object.__new__(cls)
    #     return BllUserMedicament._instance

    def __init__(self, entityType=EntityUserMedicament):
        return super().__init__(entityType)

    def isJInZhiUser(self,userId,drugId):
        entity=self.findEntity(and_(EntityUserMedicament.UserId == userId,EntityUserMedicament.DrugId == drugId))
        if(entity is None):
            return False
        else:
            return True




