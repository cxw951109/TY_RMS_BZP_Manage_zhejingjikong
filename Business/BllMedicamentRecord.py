from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityMedicamentRecord import *
from Lib.Utils import *
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading


#试剂流转记录业务逻辑类
class BllMedicamentRecord(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllMedicamentRecord, "_instance"):
    #         with BllMedicamentRecord._instance_lock:
    #             if not hasattr(BllMedicamentRecord, "_instance"):
    #                 BllMedicamentRecord._instance = object.__new__(cls)
    #     return BllMedicamentRecord._instance

    def __init__(self, entityType=EntityMedicamentRecord):
        return super().__init__(entityType)

    #获取试剂最后一次使用余量
    def getLastRecordRemain(self,drugId):
        SQL = """
        select RecordRemain from rms_medicamentrecord WHERE MedicamentId='"""+drugId+"""' ORDER BY CreateDate DESC LIMIT 1 
        """
        try:
            result= BllMedicamentRecord().execute(SQL)
            return float(result.fetchone()[0])
        except Exception as e :
            print(e)
            return 0
