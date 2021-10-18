from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

class EntityPurchaseOrderDetailed(declarative_base()):
    __tablename__ = "RMS_PurchaseOrderDetailed"

    PurchaseOrderDetailedId = Column(String(50),primary_key=True) 
    PurchaseOrderId = Column(String(50)) 
    DrugName = Column(String(50)) 
    CASNumber = Column(String(50)) 
    Speci = Column(Float) 
    SpeciUnit = Column(String(50))
    Purity = Column(String(50))
    Count = Column(Integer)
    SortIndex = Column(Integer)
    CreateDate = Column(String(50)) 
