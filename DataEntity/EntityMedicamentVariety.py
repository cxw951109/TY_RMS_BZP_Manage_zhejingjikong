from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#试剂类型实体类
class EntityMedicamentVariety(declarative_base()):
    __tablename__ = "RMS_MedicamentVariety"

    VarietyId = Column(String(50),primary_key=True) #类型ID
    CustomerId = Column(String(50)) #客户ID
    CASNumber = Column(String(50)) #试剂cas码
    Name = Column(String(50)) #试剂名称
    EnglishName = Column(String(50)) #英文名称
    Purity = Column(String(50)) #纯度
    Speci=Column(Float) #规格
    SpeciUnit=Column(String(50)) #规格单位
    Unit=Column(String(50)) #单位
    IsSupervise = Column(Integer) #是否监管
    InventoryWarningValue = Column(Integer) #库存预警量
    ShelfLifeWarningValue = Column(Integer) #保质期到期提前预警天数
    UseDaysWarningValue = Column(Integer) #领用超期预警天数
    PeriodCheckIntervalValue = Column(Integer) #期间核查间隔天数
    IsWeigh = Column(Integer)
    EmptyCount = Column(Integer) #空瓶数量
    UseCount = Column(Integer) #当前领用数量
    NormalCount = Column(Integer) #在库数量
    TotalCount = Column(Integer) #总数量
    Remark1 = Column(String(50)) #备注1
    Remark2 = Column(String(50)) #备注2
    Remark3 = Column(String(50)) #备注3
    CreateDate = Column(String(50)) #创建日期
    CreateUserId = Column(String(50)) #创建用户ID
    CreateUserName = Column(String(50)) #创建用户名称
    IsAdd = Column(Integer)