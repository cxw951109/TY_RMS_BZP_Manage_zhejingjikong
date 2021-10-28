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
from DataEntity.EntityMedicament import *
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


class BllMedicament(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    #
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllMedicament, "_instance"):
    #         with BllMedicament._instance_lock:
    #             if not hasattr(BllMedicament, "_instance"):
    #                 BllMedicament._instance = object.__new__(cls)
    #     return BllMedicament._instance

    def __init__(self, entityType=EntityMedicament):
        return super().__init__(entityType)

    #获取试剂列表
    def getDrugList(self, customerId, keyWord, pageParam):
        keyWord = '%'+keyWord+'%'
        orm_query = self.findList().filter(EntityMedicament.CustomerId == customerId
                                           ).filter(or_(EntityMedicament.RFID.like(keyWord), EntityMedicament.Name.like(keyWord))).order_by(desc(EntityMedicament.PutInStorageDate))
        return self.queryPage(orm_query, pageParam)

    # 试剂入库
    def drugPutIn(self, entityDrug=EntityMedicament(),entityClient=EntityClient(),entityUser=EntityUser()):
        entityDrugRecord = EntityMedicamentRecord()
        entityDrugRecord.RecordId = Utils.UUID()
        entityDrugRecord.CustomerId = entityClient.CustomerId
        entityDrugRecord.ClientId = entityClient.ClientId
        entityDrugRecord.ClientCode = entityClient.ClientCode
        entityDrugRecord.VarietyId = entityDrug.VarietyId
        entityDrugRecord.MedicamentId = entityDrug.MedicamentId
        entityDrugRecord.RecordRemain=entityDrug.Remain
        entityDrugRecord.Price = entityDrug.Price
        entityDrugRecord.RecordType = 1
        entityDrugRecord.IsEmpty = 0
        entityDrugRecord.CreateDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entityDrugRecord.CreateUserId = entityUser.UserId
        entityDrugRecord.CreateUserName = entityUser.RealName
        # 创建事务
        self.beginTrans()
        self.session.add(entityDrug)
        if(entityDrug.Status==1):
            self.session.add(entityDrugRecord)
        boolean_ = self.commitTrans()
        print(boolean_, 66666666666)
        return boolean_

    # 试剂领用
    def drugUse(self, entityDrug=EntityMedicament(), entityClient=EntityClient(), entityUser=EntityUser()):
        #创建事务
        self.beginTrans()
        self.session.merge(entityDrug)
        if(BllUserMedicament().isJInZhiUser(entityUser.UserId,entityDrug.MedicamentId)):
            warning_obj = EntityWarning(WarningId=str(Utils.UUID()), CustomerId=entityDrug.CustomerId,
                                        ObjectType=7, ObjectId=entityDrug.MedicamentId, ObjectName=entityDrug.Name,
                                        WarningContent= entityUser.RealName+'违规领用了试剂“'+entityDrug.Name+'”（'+entityDrug.BarCode+'）',WarningDate=datetime.datetime.now(),
                                        WarningUserName=entityUser.RealName, IsSolve=0, IsAdd=1)
            BllWarning().insert(warning_obj)
        entityDrugRecord=EntityMedicamentRecord()
        entityDrugRecord.RecordId=Utils.UUID()
        entityDrugRecord.CustomerId=entityClient.CustomerId
        entityDrugRecord.ClientId=entityClient.ClientId
        entityDrugRecord.ClientCode=entityClient.ClientCode
        entityDrugRecord.VarietyId=entityDrug.VarietyId
        entityDrugRecord.MedicamentId=entityDrug.MedicamentId
        entityDrugRecord.Price=entityDrug.Price
        entityDrugRecord.RecordType=DrugRecordType.Use
        entityDrugRecord.RecordRemain=entityDrug.Remain
        entityDrugRecord.IsEmpty=0
        entityDrugRecord.CreateDate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entityDrugRecord.CreateUserId=entityUser.UserId
        entityDrugRecord.CreateUserName=entityUser.RealName
        self.session.add(entityDrugRecord)
        entityVariety = BllMedicamentVariety().findEntity(entityDrug.VarietyId)
        entityVariety.NormalCount-=1
        entityVariety.UseCount+=1
        self.session.merge(entityVariety)
        self.commitTrans()

    # 试剂归还
    def drugReturn(self, entityDrug=EntityMedicament(), entityClient=EntityClient(), entityUser=EntityUser()):
        #创建事务
        self.beginTrans()
        self.session.merge(entityDrug)
        entityDrugRecord=EntityMedicamentRecord()
        entityDrugRecord.RecordId=Utils.UUID()
        if(entityDrug.Status!=3):
            entityDrugRecord.CustomerId=entityClient.CustomerId
            entityDrugRecord.ClientId=entityClient.ClientId
            entityDrugRecord.ClientCode=entityClient.ClientCode
            lastRemain=BllMedicamentRecord().getLastRecordRemain(entityDrug.MedicamentId)
            entityDrugRecord.UseQuantity=float(lastRemain)-float(entityDrug.Remain if entityDrug.Remain else 0)
            entityDrugRecord.RecordRemain=entityDrug.Remain
        else:
             entityDrugRecord.CustomerId=entityUser.CustomerId
             entityDrugRecord.ClientId='0'
             entityDrugRecord.ClientCode=0
             entityDrugRecord.UseQuantity=entityDrug.Remain
             entityDrugRecord.RecordRemain=0
             entityDrug.Remain=0
             self.session.merge(entityDrug)
        entityDrugRecord.VarietyId=entityDrug.VarietyId
        entityDrugRecord.MedicamentId=entityDrug.MedicamentId
        entityDrugRecord.Price=entityDrug.Price
        entityDrugRecord.RecordType=DrugRecordType.Return
        entityDrugRecord.IsEmpty=1 if(entityDrug.Status==DrugStatus.Empty) else 0
        entityDrugRecord.CreateDate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entityDrugRecord.CreateUserId=entityUser.UserId
        entityDrugRecord.CreateUserName=entityUser.RealName
        self.session.add(entityDrugRecord)
        entityVariety = BllMedicamentVariety().findEntity(entityDrug.VarietyId)
        if(entityDrug.Remain!=0):
            entityVariety.NormalCount+=1
        else:
            entityVariety.EmptyCount += 1
        entityVariety.UseCount-=1
        self.session.merge(entityVariety)

        self.commitTrans()

    #获取离保质期最近的同类试剂
    def getDrugNearExpired(self, varietyId, customerId):
        drugList = self.findList().order_by(
            desc(EntityMedicament.ExpirationDate)).limit(1)
        return drugList.first()

    #获取待归还试剂列表
    def getWaitReturnDrugList(self, customerId):
        drugList = self.findList(and_(EntityMedicament.CustomerId ==
                                      customerId, EntityMedicament.Status == DrugStatus.Out)).all()
        return drugList

    #获取待入库试剂模板
    def getWaitPutInDrugTemplateList(self, customerId, clientId):
        templateList = BllMedicamentTemplate().findList(and_(EntityMedicamentTemplate.CustomerId == customerId,
                                                             EntityMedicamentTemplate.ClientId == clientId, EntityMedicamentTemplate.IsWaitExport == 1)).all()
        return templateList

    #获取所有试剂列表
    def getAllDrugList(self, _searchWord, pageParam,clientId=''):
        queryStr=''
        queryParams={}
        if(clientId==''):
            queryStr = 'select * from RMS_Medicament where Name like :searchWord or BarCode like :searchWord or EnglishName like :searchWord or Remark1 like :searchWord or Remark2 like :searchWord or Remark3 like :searchWord or Remark4 like :searchWord order by PutInDate desc'
            queryParams = {"searchWord": '%'+_searchWord+'%'}
        else:
            queryStr = 'select * from RMS_Medicament where ClientId=:clientId and ( Name like :searchWord or BarCode like :searchWord or EnglishName like :searchWord or Remark1 like :searchWord or Remark2 like :searchWord or Remark3 like :searchWord or Remark4 like :searchWord) order by PutInDate desc'
            queryParams = {"searchWord": '%'+_searchWord+'%','clientId':clientId}       
        print('获取试剂列表',queryStr + (' limit ' + str((pageParam.curPage-1)*pageParam.pageRows)+','+str(pageParam.pageRows) if pageParam.pageRows != 0 else ''))
        templateList = self.execute(queryStr + (' limit ' + str((pageParam.curPage-1)*pageParam.pageRows)+','+str(pageParam.pageRows) if pageParam.pageRows != 0 else ''), queryParams).fetchall()
        pageParam.totalRecords = self.execute(queryStr.replace('*', 'count(*)'), queryParams).fetchone()[0]
        jsonData = Utils.mysqlTable2Model(templateList)
        return jsonData


    # 删除试剂
    def delete_drug(self, MedicamentId, medicament_obj):
        # 开启事物
        self.beginTrans()
        medicament_variety_obj = BllMedicamentVariety().findEntity(
            EntityMedicamentVariety.VarietyId == medicament_obj.VarietyId)
        medicament_variety_obj.TotalCount -= 1
        medicament_variety_obj.NormalCount -= 1
        self.session.delete(medicament_obj)
        self.session.merge(medicament_variety_obj)
        self.commitTrans()

    # 危险品信息模糊查询
    def select_danger(self, name):
        querySte = "SELECT a.ename, a.cname, a.chucunfangfa, a.yongtu, a.weight, a.xingzhiyuwendingxing, a.dangerpic,a.cas,a.formula,a.wuxing,a.dulixue, a.shengtaixue, a.othername, a.safestr FROM rms_msds a WHERE a.cname LIKE '%{}%' ORDER BY (CASE WHEN a.cname='{}' THEN 1 WHEN a.cname like '{}%' THEN 2 WHEN a.cname like '%{}%' THEN 3 WHEN a.cname like '%{}' THEN 4 ELSE 5 END) limit 0,19".format(
            name, name, name, name, name)
        templateList = self.execute(querySte).fetchall()
        jsonData = Utils.mysqlTable2Model(templateList)
        dangerData = []
        for i in jsonData:
            dangerData.append({"ename": i["ename"], "cname": i["cname"],"cas":i["cas"],"formula":i["formula"],"wuxing":i["wuxing"],"dulixue":i["dulixue"],"chucunfangfa": i["chucunfangfa"], "yongtu": i["yongtu"], "weight": i["weight"],
                              "xingzhiyuwendingxing": i["xingzhiyuwendingxing"], "dangerpic": i["dangerpic"], "shengtaixue": i["shengtaixue"], "othername": i["othername"], "safestr": i["safestr"]})
        return dangerData

    #获取推荐货道
    def get_boxlist(self,clientId,type,num=0):
        wait_num=0
        if type == 'up':
            wait_num = self.findCount(EntityMedicament.ClientId ==clientId,EntityMedicament.Status ==DrugStatus.Normal,EntityMedicament.Place =='')
            num = num +wait_num
        query = self.session.query(EntityMedicament.Place).filter(EntityMedicament.ClientId ==clientId, EntityMedicament.Place != '').all()
        query =[int(i[0]) for i in query]
        null_place =['%s' %i for i in range(1,31) if i not in query]
        if num <= len(null_place):
            return null_place[wait_num:num]
        else:
            return False

