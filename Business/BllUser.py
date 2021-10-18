from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression
from Business.Repository import *
from DataEntity.EntityUser import *
from Lib.Utils import *
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList
from sqlalchemy.sql import func
import threading


# 用户操作业务逻辑类
class BllUser(Repository):
    # _instance_lock = threading.Lock()
    # #实现单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllUser, "_instance"):
    #         with BllUser._instance_lock:
    #             if not hasattr(BllUser, "_instance"):
    #                 BllUser._instance = object.__new__(cls)
    #     return BllUser._instance

    def __init__(self, entityType=EntityUser):
        return super().__init__(entityType)

    # 用户账号密码登录
    def login(self, userAccount, userPwd):
        return self.findEntity(and_(EntityUser.Account == userAccount, EntityUser.Password == Utils.MD5(userPwd)))

    # 根据条码获取用户
    def getUserByBarCode(self, barCode):
        return self.findEntity(EntityUser.BarCode == barCode)

    # 获取用户列表
    def getUserList(self, customerId, pageParam, keyWord=''):
        keyWord = '%' + keyWord + '%'
        orm_query = self.findList().filter(EntityUser.CustomerId == customerId
                                           ).filter(
            or_(EntityUser.UserCode.like(keyWord), EntityUser.RealName.like(keyWord))).order_by(
            desc(EntityUser.CreateDate))
        return self.queryPage(orm_query, pageParam)

    # # 获取用户列表
    # def getUserList(self, customerId, pageParam, number, role, user_type, name, keyWord=''):
    #     keyWord = '%' + keyWord + '%'
    #     # orm_query = self.findList().filter(EntityUser.CustomerId == customerId).filter(and_((number if EntityUser.UserCode.like(number) else ""), (name if EntityUser.RealName.like(name) else ""), (role if EntityUser.RoleName == role else ""), (user_type if EntityUser.IsEnabled == user_type else ""))).order_by(desc(EntityUser.CreateDate))
    #     orm_query = self.findList()
    #     if (len(number) != 0):
    #         orm_query = orm_query.filter(EntityUser.UserCode.like(number))
    #     if (len(role) != 0):
    #         orm_query = orm_query.filter(EntityUser.RoleName == role)
    #     if (len(user_type) != 0):
    #         orm_query = orm_query.filter(EntityUser.IsEnabled == user_type)
    #     if (len(name) != 0):
    #         orm_query = orm_query.filter(EntityUser.RealName.like(name))
    #     orm_query = orm_query.order_by(desc(EntityUser.CreateDate))
    #
    #     return self.queryPage(orm_query, pageParam)

    # 获取用户详情信息
    def getUserInfo(self, userId):
        return self.findEntity(userId)

    # 模糊查询获取用户列表
    def like_user_list(self, searchWord):
        return self.findList(or_(EntityUser.UserCode.like('%' + searchWord + '%'),
                                 EntityUser.RealName.like('%' + searchWord + '%'))).all()

    # 获取用户列表
    def getSelectUserList(self):
        userList = self.findList().order_by(desc(EntityUser.CreateDate)).all()
        selectList = [{'name': x.RealName + '(' + x.UserCode + ')', 'value': x.UserId} for x in userList]
        return selectList
