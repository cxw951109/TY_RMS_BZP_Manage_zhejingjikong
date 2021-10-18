from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityMedicamentVariety import *
from DataEntity.EntityUser import *
from Lib.Utils import *
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading


#试剂品种业务逻辑类
class BllMedicamentVariety(Repository):
    _instance_lock = threading.Lock()
    # #实现单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllMedicamentVariety, "_instance"):
    #         with BllMedicamentVariety._instance_lock:
    #             if not hasattr(BllMedicamentVariety, "_instance"):
    #                 BllMedicamentVariety._instance = object.__new__(cls)
    #     return BllMedicamentVariety._instance

    def __init__(self, entityType=EntityMedicamentVariety):
        return super().__init__(entityType)

    #创建试剂品种
    def createDrugVariety(self,customerId,name, english, casNumber,purity,unit,speciUnit,speci,entityUser=EntityUser()):
        entity = self.findEntity(and_(EntityMedicamentVariety.Name == name,EntityMedicamentVariety.Purity == purity
                                      ,EntityMedicamentVariety.Unit == unit,EntityMedicamentVariety.SpeciUnit == speciUnit,EntityMedicamentVariety.Speci == speci))

        if(entity is None):
            print(entity, 9999999999999999999)
            entity=EntityMedicamentVariety()
            entity.VarietyId=str(Utils.UUID())
            entity.CustomerId=customerId
            entity.InventoryWarningValue=10
            entity.ShelfLifeWarningValue=10
            entity.UseDaysWarningValue=10
            entity.Name=name
            entity.EnglishName=english
            entity.CASNumber=casNumber
            entity.Purity=purity
            entity.Unit=unit
            entity.SpeciUnit=speciUnit
            # 库存总数
            entity.TotalCount = 1
            # 在库数量
            entity.NormalCount = 1
            # 领用数量
            entity.UseCount = 0
            # 空瓶数量
            entity.EmptyCount = 0
            entity.IsSupervise=0
            entity.Speci=speci
            entity.CreateDate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entity.CreateUserId=entityUser.UserId
            entity.CreateUserName=entityUser.RealName
            self.insert(entity)
        # else:
        #     # 库存总数 + 1
        #     entity.TotalCount += 1
        #     # 在库数量 + 1
        #     entity.NormalCount += 1
        #     self.update(entity)
        entity = self.session.merge(entity)
        return entity


    # 模糊查询根据试剂名称或英文名称查询
    def findEnglishOrChinseNameList(self, params):
        return self.findList(or_(EntityMedicamentVariety.Name.like('%' + params + '%'),
                                                               EntityMedicamentVariety.EnglishName.like('%' + params + '%')))
