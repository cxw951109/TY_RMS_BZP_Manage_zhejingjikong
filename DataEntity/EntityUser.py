from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
import types

#用户信息实体类
class EntityUser(declarative_base()):
    __tablename__ = "RMS_User"

    UserId = Column(String(50),primary_key=True) # 用户ID
    CustomerId = Column(String(50)) # 客户ID
    RoleId = Column(String(50)) # 角色ID
    RoleName = Column(String(50)) # 角色名称
    BarCode = Column(String(50)) # 条码
    UserCode = Column(String(50)) # 用户编号
    Account = Column(String(50)) # 账户
    Password = Column(String(50)) # 密码
    RealName = Column(String(50)) # 真实名称
    AvatarUrl = Column(String(50)) # 头像图片地址
    SignUrl = Column(String(500)) # 签名图片地址
    AvatarBase64 = Column(Text) # 头像base64值
    Sex = Column(Integer) # 性别
    Birthday = Column(String(50)) # 生日
    Mobile = Column(String(50)) # 手机号码
    Email = Column(String(50)) # Enail
    QQ = Column(String(50)) # QQ
    IsEnabled = Column(Integer) # 是否启用
    FirstVisitDate = Column(String(50)) # 首次登陆日期
    LastVisitDate = Column(String(50)) # 最后登陆日期
    Description = Column(String(50)) # 备注
    CreateDate = Column(String(50)) # 创建日期
    CreateUserId = Column(String(50)) # 创建用户ID
    CreateUserName = Column(String(50)) # 创建用户名称
    IsAdd = Column(Integer)