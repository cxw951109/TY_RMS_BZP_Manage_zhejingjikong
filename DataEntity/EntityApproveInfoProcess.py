from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

class EntityApproveInfoProcess(declarative_base()):
    __tablename__ = "RMS_ApproveInfoProcess"

    Id = Column(String(50),primary_key=True)
    ApproveTypeId = Column(String(50))
    ApproveInfoId = Column(String(50))
    ApproveUserId = Column(String(50))
    ApproveUserName = Column(String(50))
    ApproveStatus = Column(Integer) # 1:未开始 2:处理中 3:已完成通过 4:已完成未通过
    ApproveComment = Column(String(200))
    ApproveDate = Column(String(50))
    SortIndex = Column(Integer)
