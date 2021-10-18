from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#试剂信息实体类
class EntityMedicamentApprove(declarative_base()):
    __tablename__ = "RMS_MedicamentApprove"

    MedicamentId = Column(String(50),primary_key=True) #试剂ID
    VarietyId = Column(String(50)) #试剂类型ID
    BarCode = Column(String(50)) #条码
    ClientId = Column(String(50)) #终端ID
    ClientCode = Column(String(50)) #终端编号
    CustomerId = Column(String(50)) #客户ID
    CASNumber = Column(String(50)) #试剂cas码
    Name = Column(String(50)) #试剂名称
    EnglishName = Column(String(50)) #英文名称
    Speci=Column(Float) #规格
    SpeciUnit=Column(String(50)) #规格单位
    Unit=Column(String(50)) #单位
    Remain=Column(String(50)) #库存余量
    Manufacturer = Column(String(50)) #生产厂商 
    ImageUrl = Column(String(50)) #图片地址
    Distributor = Column(String(50)) #销售商
    ProductionDate = Column(String(50)) #生产日期
    ExpirationDate = Column(String(50)) #过期日期
    ShelfLife = Column(Integer) #保质期
    ShelfLifeWarningValue = Column(Integer) #保质期到期提前预警天数 
    UseDaysWarningValue = Column(Integer) #使用超期预警天数
    IsWeigh = Column(Integer)
    WeighFlag = Column(Integer)
    Purity = Column(String(50)) #试剂纯度
    Price = Column(String(50)) #价格
    Place = Column(String(50)) #位置
    Status = Column(Integer) #当前状态（1：在库 2：出库 3：空瓶）
    IsSupervise = Column(Integer) #是否监管
    ByUserDate = Column(String(50)) #最后使用日期
    ByUserId = Column(String(50)) #最后使用人ID
    ByUserName = Column(String(50)) #最后使用人名称
    PutInDate = Column(String(50)) #入库日期
    PutInUserId = Column(String(50)) #入库用户ID
    PutInUserName = Column(String(50)) #入库用户名
    Remark1 = Column(String(50)) #备注1
    Remark2 = Column(String(50)) #备注2
    Remark3 = Column(String(50)) #备注3
    Remark4 = Column(String(50))
    Remark5 = Column(String(50))
    Remark6 = Column(String(50))
    Remark7 = Column(String(50))
    Remark8 = Column(String(50))
    Remark9 = Column(String(50))
    Remark10 = Column(String(50))
    
    IsAdd = Column(Integer)