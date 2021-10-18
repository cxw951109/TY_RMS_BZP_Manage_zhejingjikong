from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

class EntityApproveType(declarative_base()):
    __tablename__ = "RMS_ApproveType"

    ApproveTypeId = Column(String(50),primary_key=True) 
    ApproveTypeCode = Column(String(50)) 
    ApproveTypeName = Column(String(50)) 
    SortIndex = Column(String(50)) 
    Description = Column(String(50)) 
    CreateDate = Column(String(50)) 
