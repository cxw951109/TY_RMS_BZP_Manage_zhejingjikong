from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from Business.BllUser import *
from Business.BllMedicament import *
from Business.BllMedicamentApprove import *
from Business.BllPurchaseOrder import *
from Business.BllApproveType import *
from Business.BllApproveTypeProcess import *
from Business.BllApproveInfoProcess import *
from DataEntity.EntityApproveType import *
from DataEntity.EntityApproveTypeProcess import *
from DataEntity.EntityApproveInfo import *
from DataEntity.EntityApproveInfoProcess import *
from DataEntity.EntityMedicamentApprove import *
from Lib.Utils import *
from Lib.Model import *

import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import threading

class BllApproveInfo(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    #
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllLog, "_instance"):
    #         with BllLog._instance_lock:
    #             if not hasattr(BllLog, "_instance"):
    #                 BllLog._instance = object.__new__(cls)
    #     return BllLog._instance


    def __init__(self, entityType=EntityApproveInfo):
        return super().__init__(entityType)

    # 添加审批
    def addApproveInfo(self,approveTypeCode,approveInfoContent,objectId,objectCode,approveCause,createUserId):
        approveType=BllApproveType().findEntity(EntityApproveType.ApproveTypeCode==approveTypeCode)
        approveTypeProcessList=BllApproveTypeProcess().findList(EntityApproveTypeProcess.ApproveTypeId==approveType.ApproveTypeId).all()
        createUser=BllUser().findEntity(createUserId)
        approveInfoId=Utils.UUID()
        approveInfoEntity=EntityApproveInfo(ApproveInfoId=approveInfoId,ApproveInfoCode='60'+Utils.createOrderCode(),ApproveTypeId=approveType.ApproveTypeId,
                          ApproveTypeCode=approveTypeCode,ApproveTypeName=approveType.ApproveTypeName,ApproveInfoTitle=approveCause,
                          ApproveObjectId=objectId,ApproveObjectCode=objectCode,ApproveTotalStepCount=len(approveTypeProcessList),
                          ApproveInfoContent=approveInfoContent,ApproveCompleteStepCount=0,ApproveCurStepIndex=0,ApproveStatus=1,
                          CreateDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),CreateUserId=createUser.UserId,
                          CreateUserName='{0}({1})'.format(createUser.RealName,createUser.UserCode))
        BllApproveInfo().insert(approveInfoEntity)
        for approveTypeProcess in approveTypeProcessList:
            approveInfoProcessEntity=EntityApproveInfoProcess(Id=Utils.UUID(),ApproveTypeId=approveType.ApproveTypeId,
                                 ApproveInfoId=approveInfoId,ApproveUserId=approveTypeProcess.ObjectId,
                                 ApproveUserName=approveTypeProcess.ObjectName,ApproveStatus=1,
                                 SortIndex=approveTypeProcess.SortIndex)
            BllApproveInfoProcess().insert(approveInfoProcessEntity)

        self.submitApprovalAndNextStep(approveInfoId,True,'',createUserId)
        return approveInfoId

    def ceshissssss():
        pass

    # 审批并转到下一步下一审批步骤
    def submitApprovalAndNextStep(self,approveInfoId,isArgee,comment,approvalUserId):
        approveInfoEntity=BllApproveInfo().findEntity(approveInfoId)
        if(approveInfoEntity.ApproveStatus == ApproveAllStatus.Agree or approveInfoEntity.ApproveStatus== ApproveAllStatus.Overrule):
            return 101      
        approveInfoProcessList=BllApproveInfoProcess().findList(EntityApproveInfoProcess.ApproveInfoId==approveInfoId).all()
        if(approveInfoEntity.ApproveCurStepIndex!=0):
            curApproveProcess= [x for x in approveInfoProcessList if x.SortIndex==approveInfoEntity.ApproveCurStepIndex]
            curApproveProcess=curApproveProcess[0]
            if(approvalUserId!=curApproveProcess.ApproveUserId):
                raise Exception('setApprovalAndNextStep:当前用户没有权限进行此步骤审批！')
            curApproveProcess.ApproveStatus=ApproveAllStatus.Agree if isArgee else ApproveAllStatus.Overrule
            curApproveProcess.ApproveComment=comment
            curApproveProcess.ApproveDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            BllApproveInfoProcess().update(curApproveProcess)

            if(not isArgee):
                approveInfoEntity.ApproveStatus=ApproveAllStatus.Overrule
                approveInfoEntity.ApproveCompleteStepCount=approveInfoEntity.ApproveTotalStepCount
            elif(approveInfoEntity.ApproveCurStepIndex==len(approveInfoProcessList)):
                approveInfoEntity.ApproveStatus=ApproveAllStatus.Agree
            else:
                approveInfoEntity.ApproveStatus=ApproveAllStatus.Waiting
            approveInfoEntity.ApproveCompleteStepCount+=1
            BllApproveInfo().update(approveInfoEntity)
            if(approveInfoEntity.ApproveStatus == ApproveAllStatus.Agree or approveInfoEntity.ApproveStatus== ApproveAllStatus.Overrule):
                if(approveInfoEntity.ApproveTypeCode==ApproveTypeAllCode.Purchase):
                    purchaseOrderEntity=BllPurchaseOrder().findEntity(approveInfoEntity.ApproveObjectId)
                    purchaseOrderEntity.PurchaseOrderStatus=approveInfoEntity.ApproveStatus
                    BllPurchaseOrder().update(purchaseOrderEntity)
                elif(approveInfoEntity.ApproveTypeCode==ApproveTypeAllCode.DrugEdit):
                    oldDurgEntity=BllMedicament().findEntity(approveInfoEntity.ApproveObjectId)
                    newDurgEntity=BllMedicamentApprove().findEntity(approveInfoEntity.ApproveObjectId)
                    newDurgEntity.__dict__["_sa_instance_state"]=oldDurgEntity.__dict__["_sa_instance_state"]
                    BllMedicament().update(newDurgEntity)
                    BllMedicamentApprove().delete(EntityMedicamentApprove.MedicamentId==approveInfoEntity.ApproveObjectId)
                return 0        
                

        isHasWaitApproveProcess=False # 是否有待审批流程
        for approveInfoProcess in approveInfoProcessList:
            if(approveInfoProcess.ApproveStatus==ApproveAllStatus.Waiting):
                isHasWaitApproveProcess=True

        if(isHasWaitApproveProcess):
            raise Exception('setApprovalAndNextStep:存在未审批步骤，不能转到下一步！')
        
        setWaitApproveIndex=approveInfoEntity.ApproveCurStepIndex+1 # 设置审批序号
        if(setWaitApproveIndex>len(approveInfoProcessList)):
            return 102

        setApproveProcess= [x for x in approveInfoProcessList if x.SortIndex==setWaitApproveIndex]
        setApproveProcess=setApproveProcess[0]
        setApproveProcess.ApproveStatus=ApproveAllStatus.Waiting
        BllApproveInfoProcess().update(setApproveProcess)

        approveInfoEntity.ApproveCurStepIndex+=1
        approveInfoEntity.ApproveCurAcceptUserId=setApproveProcess.ApproveUserId
        approveInfoEntity.ApproveCurAcceptUserName=setApproveProcess.ApproveUserName
        BllApproveInfo().update(approveInfoEntity)

        return 0

