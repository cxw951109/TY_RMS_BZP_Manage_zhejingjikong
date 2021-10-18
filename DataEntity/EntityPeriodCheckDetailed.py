from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

class EntityPeriodCheckDetailed(declarative_base()):
    __tablename__ = "RMS_PeriodCheckDetailed"

    PeriodCheckDetailedId = Column(String(50),primary_key=True)
    PeriodCheckId = Column(String(50))
    PeriodCheckCode = Column(String(50))
    DrugId = Column(String(50))
    PeriodCheckMethod = Column(String(50))
    Status = Column(Integer) # 1:不合格 2:合格
    Description = Column(String(255))
    SortIndex = Column(Integer)
    CreateDate = Column(String(50))
    CreateUserId = Column(String(50))
    CreateUserName = Column(String(50))
