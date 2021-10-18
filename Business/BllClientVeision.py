from sqlalchemy import or_, desc

from Business.Repository import *
from DataEntity.EntityClientVersion import EntityClientVersion


class BllClientVersion(Repository):

    def __init__(self, entity=EntityClientVersion):
        return super().__init__(entity)

    # 获取搜索按名称、版本号、创建人搜索的列表
    def get_search_list(self, search_word):
        search_word = '%' + search_word + '%'
        return self.findList(or_(EntityClientVersion.CreateUserName.like(search_word),
                          EntityClientVersion.VersionCode.like(search_word),
                          EntityClientVersion.VersionName.like(search_word))).order_by(desc(EntityClientVersion.CreateDate)).all()
