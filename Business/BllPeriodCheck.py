from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityPeriodCheck import *
from DataEntity.EntityPeriodCheckDetailed import *
from Lib.Utils import *
from Lib.Model import *

import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading

class BllPeriodCheck(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    #
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllLog, "_instance"):
    #         with BllLog._instance_lock:
    #             if not hasattr(BllLog, "_instance"):
    #                 BllLog._instance = object.__new__(cls)
    #     return BllLog._instance


    def __init__(self, entityType=EntityPeriodCheck):
        return super().__init__(entityType)

    # # 获取期间核查数据列表
    # def getPeriodCheckList(self,pageParam,PeriodCheckCode='',CreateUserName='',PeriodCheckStatus=''):
    #     orm_query= self.findList().order_by(desc(EntityPeriodCheck.CreateDate))
    #     if(PeriodCheckCode):
    #         orm_query= orm_query.filter(EntityPeriodCheck.PeriodCheckCode.like('%'+PeriodCheckCode+'%'))
    #     if(CreateUserName):
    #         orm_query= orm_query.filter(EntityPeriodCheck.CreateUserName.like('%'+CreateUserName+'%'))
    #     if(PeriodCheckStatus):
    #         orm_query= orm_query.filter(EntityPeriodCheck.PeriodCheckStatus==int(PeriodCheckStatus))
    #     return self.queryPage(orm_query,pageParam)

    # 获取期间核查数据列表
    def getPeriodCheckList(self,pageParam,PeriodCheckCode='',CreateUserName='',PeriodCheckStatus=''):
        SQL="""
            SELECT * FROM(
            SELECT a.*,COUNT(b.MedicamentId) AS PeriodCurrentDrugCount, SUM(CASE WHEN TO_DAYS(date_add(b.LastPeriodCheckDate, interval a.PeriodCheckIntervalValue day)) <= TO_DAYS(NOW()) THEN 1 ELSE 0 END) AS NotPeriodCheckTotalCount,
            SUM(CASE WHEN b.LastPeriodCheckStatus=1 THEN 1 ELSE 0 END) AS PeriodCheckProblemsCount
            FROM rms_medicamentvariety a  LEFT JOIN(
            SELECT MedicamentId,VarietyId ,LastPeriodCheckStatus,(CASE WHEN LastPeriodCheckDate THEN LastPeriodCheckDate ELSE PutInDate  END) AS LastPeriodCheckDate  FROM rms_medicament) b
            ON a.VarietyId=b.VarietyId GROUP BY a.VarietyId ORDER BY NotPeriodCheckTotalCount DESC
            )nt
        """
        queryParams={}
        info_list=self.execute(SQL+ ' limit '+ str((pageParam.curPage-1)*pageParam.pageRows)+','+str(pageParam.pageRows),queryParams).fetchall()
        pageParam.totalRecords=self.execute(SQL.replace('*','count(*)',1),queryParams).fetchone()[0]
        info_list = Utils.mysqlTable2Model(info_list)
        data = info_list
        return data
