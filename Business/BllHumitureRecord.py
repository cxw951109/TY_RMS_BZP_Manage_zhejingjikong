from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityMedicamentVariety import *
from DataEntity.EntityUser import *
from DataEntity.EntityModule import *
from DataEntity.EntityHumitureRecord import *
from Lib.Utils import *


import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading


# 功能模块

# 功能模块
class BllHumitureRecord(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllHumitureRecord, "_instance"):
    #         with BllHumitureRecord._instance_lock:
    #             if not hasattr(BllHumitureRecord, "_instance"):
    #                 BllHumitureRecord._instance = object.__new__(cls)
    #     return BllHumitureRecord._instance

    def __init__(self, entityType=EntityHumitureRecord):
        return super().__init__(entityType)

    #获取温湿度列表
    def getHumitureList(self,customerId,pageParam):
        queryStr='select * from ((select * from RMS_HumitureRecord where ClientId=:clientId) '
        queryStr+=' union all (select * from RMS_HumitureRecord where ClientId!=:clientId  order by ClientName ASC ) )t order by t.RecordDate DESC '

        queryCountStr='select COUNT(*) from ((select * from RMS_HumitureRecord where ClientId=:clientId) '
        queryCountStr+=' union all (select * from RMS_HumitureRecord where ClientId!=:clientId  order by ClientName ASC ) )t order by t.RecordDate DESC '
        queryParams={"clientId":CurrentInfo.ClientInfo.ClientId}
        templateList=self.execute(queryStr+ ' limit '+ str((pageParam.curPage-1)*pageParam.pageRows)+','+str(pageParam.pageRows),queryParams).fetchall()
        pageParam.totalRecords=self.execute(queryCountStr,queryParams).fetchone()[0]
        jsonData=Utils.mysqlTable2Model(templateList)
        return jsonData

    def insert_one(self, entity):
        self.insert(entity)

if __name__ == '__main__':
    for x in range(100000):
        en = EntityHumitureRecord(RecordId=str(Utils.UUID()), DeviceId='', ClientId='72e70542-b70d-11e8-aea5-448a5bc6c418',
                             ClientName='1号终端', CustomerId='', Temperature='30', Humidity='50', RecordDate=datetime.datetime.now(), IsAdd=1)
        BllHumitureRecord().insert_one(en)
