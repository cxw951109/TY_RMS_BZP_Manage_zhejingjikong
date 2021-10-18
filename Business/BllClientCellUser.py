import threading

from Business.Repository import *
from DataEntity.EntityClientCellUser import *
from DataEntity.EntityClient import *


class BllClientCellUser(Repository):
    _instance_lock = threading.Lock()
    #实现单例模式

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(BllClientUser, "_instance"):
    #         with BllClientUser._instance_lock:
    #             if not hasattr(BllClientUser, "_instance"):
    #                 BllClientUser._instance = object.__new__(cls)
    #     return BllClientUser._instance


    def __init__(self, entityType=EntityClientCellUser):
        return super().__init__(entityType)


