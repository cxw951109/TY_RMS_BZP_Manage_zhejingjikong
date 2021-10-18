from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#用户试剂
class EntityUserMedicament(declarative_base()):
    __tablename__ = "RMS_UserMedicament"

    Id = Column(String(50),primary_key=True)
    UserId = Column(String(50))
    DrugId = Column(String(50))
