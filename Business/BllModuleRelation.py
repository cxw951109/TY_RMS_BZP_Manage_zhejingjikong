from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityMedicamentVariety import *
from DataEntity.EntityUser import *
from DataEntity.EntityModule import *
from DataEntity.EntityModuleRelation import *
from Lib.Utils import *

import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading


# 功能模块
class BllModuleRelation(Repository):
    _instance_lock = threading.Lock()
    # #实现单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllModuleRelation, "_instance"):
    #         with BllModuleRelation._instance_lock:
    #             if not hasattr(BllModuleRelation, "_instance"):
    #                 BllModuleRelation._instance = object.__new__(cls)
    #     return BllModuleRelation._instance

    def __init__(self, entityType=EntityModuleRelation):
        return super().__init__(entityType)
