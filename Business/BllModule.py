from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityMedicamentVariety import *
from DataEntity.EntityUser import *
from DataEntity.EntityModule import *
from Lib.Utils import *

import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading


# 功能模块
class BllModule(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllModule, "_instance"):
    #         with BllModule._instance_lock:
    #             if not hasattr(BllModule, "_instance"):
    #                 BllModule._instance = object.__new__(cls)
    #     return BllModule._instance

    def __init__(self, entityType=EntityModule):
        return super().__init__(entityType)
