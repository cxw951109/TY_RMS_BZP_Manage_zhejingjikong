from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from Business.BllMedicamentRecord import *
from Business.BllUserMedicament import *
from Business.BllWarning import *
from Business.BllMedicamentVariety import *
from Business.BllMedicamentTemplate import *
from DataEntity.EntityMedicamentTemplate import *
from DataEntity.EntityMedicamentApprove import *
from DataEntity.EntityMedicamentVariety import *
from DataEntity.EntityMedicamentRecord import *
from DataEntity.EntityClient import *
from DataEntity.EntityWarning import *
from DataEntity.EntityUser import *
from Lib.Utils import *
import datetime
from Lib.Model import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList
from sqlalchemy.sql import func, text
import threading

#试剂流程业务逻辑类


class BllMedicamentApprove(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    #
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllMedicament, "_instance"):
    #         with BllMedicament._instance_lock:
    #             if not hasattr(BllMedicament, "_instance"):
    #                 BllMedicament._instance = object.__new__(cls)
    #     return BllMedicament._instance

    def __init__(self, entityType=EntityMedicamentApprove):
        return super().__init__(entityType)

