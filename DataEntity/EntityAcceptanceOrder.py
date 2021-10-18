from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

class EntityAcceptanceOrder(declarative_base()):
    __tablename__ = "RMS_AcceptanceOrder"

    AcceptanceOrderId = Column(String(50),primary_key=True) 
    AcceptanceOrderCode = Column(String(50)) 
    AcceptanceOrderContent = Column(Text) 
    AcceptanceOrderDrugInfo = Column(Text) 
    AcceptanceOrderTotalCount = Column(Integer) 
    AcceptanceOrderStatus = Column(Integer) 
    AcceptanceOrderImageUrl = Column(String(255))
    Description = Column(String(255))
    CreateDate = Column(String(50))
    CreateUserId = Column(String(50))
    CreateUserName = Column(String(50))
    AcceptanceDate = Column(String(50))
    AcceptanceUserId = Column(String(50))
    AcceptanceUserName = Column(String(50))
    AcceptanceComment = Column(String(255)) 
