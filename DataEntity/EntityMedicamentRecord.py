from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#试剂流转记录实体类
class EntityMedicamentRecord(declarative_base()):
    __tablename__ = "RMS_MedicamentRecord"

    RecordId = Column(String(50),primary_key=True) #流转记录ID
    ClientId = Column(String(50)) #终端ID
    ClientCode = Column(String(50)) #终端编号
    CustomerId = Column(String(50)) #客户ID
    VarietyId = Column(String(50)) #试剂类型ID
    MedicamentId = Column(String(50)) #试剂ID
    RecordType = Column(Integer) #记录类型（1：入库 2：领用 3：归还）
    Price = Column(Float) #试剂价格
    RecordRemain = Column(Float) #试剂使用余量
    UseQuantity = Column(Float) #试剂单次使用量
    IsEmpty = Column(Integer) #是否空瓶
    CreateDate = Column(String(50)) #创建日期
    CreateUserId = Column(String(50)) #创建人ID
    CreateUserName = Column(String(50)) #创建人名称
    IsAdd = Column(Integer)