from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

class EntityApproveTypeProcess(declarative_base()):
    __tablename__ = "RMS_ApproveTypeProcess"

    Id = Column(String(50),primary_key=True) 
    ApproveTypeId = Column(String(50))
    ObjectId = Column(String(50))
    ObjectName = Column(String(50)) 
    ObjectType = Column(String(50)) 
    SortIndex = Column(Integer) 
    CreateDate = Column(String(50)) 
