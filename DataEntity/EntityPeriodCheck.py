from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

class EntityPeriodCheck(declarative_base()):
    __tablename__ = "RMS_PeriodCheck"

    PeriodCheckId = Column(String(50),primary_key=True)
    PeriodCheckCode = Column(String(50))
    PeriodCheckTitle = Column(String(50))
    PeriodCheckContent = Column(Text)
    PeriodCurrentDrugCount = Column(Integer)
    PeriodCheckTotalCount = Column(Integer)
    PeriodCheckProblemsCount = Column(Integer)
    PeriodCheckStatus = Column(Integer)
    Description = Column(String(255))
    SortIndex = Column(Integer)
    CreateDate = Column(String(50))
    CreateUserId = Column(String(50))
    CreateUserName = Column(String(50))
    CompleteDate = Column(String(50))
