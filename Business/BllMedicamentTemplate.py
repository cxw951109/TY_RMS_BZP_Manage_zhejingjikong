from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityMedicamentTemplate import *
from Lib.Utils import *
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading


#试剂品种业务逻辑类
class BllMedicamentTemplate(Repository):
    _instance_lock = threading.Lock()
    # #实现单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllMedicamentTemplate, "_instance"):
    #         with BllMedicamentTemplate._instance_lock:
    #             if not hasattr(BllMedicamentTemplate, "_instance"):
    #                 BllMedicamentTemplate._instance = object.__new__(cls)
    #     return BllMedicamentTemplate._instance

    def __init__(self, entityType=EntityMedicamentTemplate):
        return super().__init__(entityType)

    # 获取所有模板列表
    def getAllTemplateList(self,pageParam,TemplateName,CreateUserName,TemplateContent,ClientId):
        orm_query= self.findList(EntityMedicamentTemplate.IsWaitExport==1).order_by(desc(EntityMedicamentTemplate.CreateDate))
        if(TemplateName):
            orm_query= orm_query.filter(EntityMedicamentTemplate.TemplateName.like('%'+TemplateName+'%'))
        if(CreateUserName):
            orm_query= orm_query.filter(EntityMedicamentTemplate.CreateUserName.like('%'+CreateUserName+'%'))
        if(TemplateContent):
            orm_query= orm_query.filter(EntityMedicamentTemplate.TemplateContent.like('%'+TemplateContent+'%'))
        if(ClientId):
            orm_query= orm_query.filter(EntityMedicamentTemplate.ClientId==ClientId)
        return self.queryPage(orm_query,pageParam)
