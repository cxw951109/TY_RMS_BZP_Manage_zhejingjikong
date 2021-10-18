from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

class EntityAcceptanceOrderDetailed(declarative_base()):
    __tablename__ = "RMS_AcceptanceOrderDetailed"

    AcceptanceOrderDetailedId = Column(String(50),primary_key=True) 
    AcceptanceOrderId = Column(String(50)) 
    DrugName = Column(String(50))
    DrugCode = Column(String(50))
    CASNumber = Column(String(50)) 
    Speci = Column(Float) 
    SpeciUnit = Column(String(50))
    Purity = Column(String(50))
    Batch = Column(String(50))
    PackageStatus = Column(String(50))
    MarkStatus = Column(String(50))
    CertificateStatus = Column(String(50))
    CertCharaValue = Column(String(50))
    CertUncertainty = Column(String(50))
    DetectionMethod = Column(String(50))
    DetectionCharaValue = Column(String(50))
    DetectionUncertainty = Column(String(50))
    BasicComponent = Column(String(50))
    StorageConditions = Column(String(50))
    Security = Column(String(50))
    SpecialRequirements = Column(String(50))
    Manufacturer = Column(String(50))
    ProductionDate = Column(String(50))
    ExpirationDate = Column(String(50))
    BuyDate = Column(String(50))
    Count = Column(Integer)
    SortIndex = Column(Integer)
    CreateDate = Column(String(50))
    AcceptanceDate = Column(String(50))
    AcceptanceUserId = Column(String(50))
    AcceptanceUserName = Column(String(50))
    AcceptanceComment = Column(String(50))
