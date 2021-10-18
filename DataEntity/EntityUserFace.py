from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#用户人脸信息实体类
class EntityUserFace(declarative_base()):
    __tablename__ = "RMS_UserFace"

    FaceId = Column(String(50),primary_key=True)
    CustomerId = Column(String(50))
    UserId = Column(String(50))
    FaceValue = Column(BLOB)
