from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

class EntityApproveInfo(declarative_base()):
    __tablename__ = "RMS_ApproveInfo"

    ApproveInfoId = Column(String(50),primary_key=True) 
    ApproveTypeId = Column(String(50))
    ApproveInfoCode = Column(String(50)) 
    ApproveTypeCode = Column(String(50)) 
    ApproveTypeName = Column(String(50)) 
    ApproveInfoTitle = Column(String(50)) 
    ApproveInfoContent = Column(Text) 
    ApproveObjectId = Column(String(50))
    ApproveObjectCode = Column(String(50)) 
    ApproveTotalStepCount = Column(Integer)
    ApproveCompleteStepCount = Column(Integer)
    ApproveCurStepIndex = Column(Integer) #从1开始
    ApproveStatus = Column(Integer) # 1:未开始 2:处理中 3:已完成通过 4:已完成未通过
    ApproveCurAcceptUserId = Column(String(50))
    ApproveCurAcceptUserName = Column(String(50))
    CreateDate = Column(String(50)) 
    CreateUserId = Column(String(50)) 
    CreateUserName = Column(String(50)) 
