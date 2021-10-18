from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#试剂入库模板实体类
class EntityMedicamentTemplate(declarative_base()):
    __tablename__ = "RMS_MedicamentTemplate"

    TemplateId = Column(String(50),primary_key=True) #模板ID
    CustomerId = Column(String(50)) #客户ID
    ClientId = Column(String(50)) #终端ID
    ClientName = Column(String(50)) #终端名称
    TemplateName = Column(String(50)) #模板名称
    TemplateContent = Column(Text) #模板内容
    IsWaitExport = Column(Integer) #是否等待导入
    CreateDate = Column(String(50)) #创建日期
    CreateUserId = Column(String(50)) #创建用户ID
    CreateUserName = Column(String(50)) #创建用户名
    IsAdd = Column(Integer)
    BarCodeCount = Column(Integer)  # 条形码数量
    StartBarCode = Column(String(50))  # 开始条形码



    #TemplateBase64 差这个字段

