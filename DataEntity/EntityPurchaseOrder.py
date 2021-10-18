from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

class EntityPurchaseOrder(declarative_base()):
    __tablename__ = "RMS_PurchaseOrder"

    PurchaseOrderId = Column(String(50),primary_key=True) 
    ApproveInfoId = Column(String(50)) 
    PurchaseOrderCode = Column(String(50)) 
    PurchaseOrderContent = Column(Text) 
    PurchaseOrderDrugInfo = Column(Text) 
    PurchaseOrderTotalCount = Column(Integer) 
    PurchaseOrderStatus = Column(Integer) 
    Description = Column(String(255))
    CreateDate = Column(String(50))
    CreateUserId = Column(String(50))
    CreateUserName = Column(String(50))
    IsCompletePurchase = Column(Integer)
    PurchaseDate = Column(String(50))
    PurchaseUserId = Column(String(50))
    PurchaseUserName = Column(String(50)) 
