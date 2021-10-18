from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityUserFace import *
from Lib.Utils import *
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading


#用户人脸信息操作业务逻辑类
class BllUserFace(Repository):
    _instance_lock = threading.Lock()
    #实现单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(BllUserFace, "_instance"):
            with BllUserFace._instance_lock:
                if not hasattr(BllUserFace, "_instance"):
                    BllUserFace._instance = object.__new__(cls)  
        return BllUserFace._instance

    def __init__(self, entityType=EntityUserFace):
        return super().__init__(entityType)

    def getFaceList(self,customerId):
        return BllUserFace().findList(EntityUserFace.CustomerId==customerId).all()



