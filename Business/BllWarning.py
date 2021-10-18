from Business.Repository import *
from DataEntity.EntityWarning import *
from Lib.Utils import *

import threading


# 功能模块
class BllWarning(Repository):
    _instance_lock = threading.Lock()
    # #实现单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllWarning, "_instance"):
    #         with BllWarning._instance_lock:
    #             if not hasattr(BllWarning, "_instance"):
    #                 BllWarning._instance = object.__new__(cls)
    #     return BllWarning._instance

    def __init__(self, entityType=EntityWarning):
        return super().__init__(entityType)

    # 定义通过搜索预警对象进行模糊查询
    def like_warning_list(self, searchValue):
        return self.findList(or_(EntityWarning.ObjectName.like('%' + searchValue + '%'), EntityWarning.WarningContent.like('%' + searchValue + '%'))).order_by(desc(EntityWarning.WarningDate), desc(EntityWarning.IsSolve)).all()
