import json
import time
import os


class GetDrugTypeData:

    # 初始化只打开一次
    data = None

    @classmethod
    def init(cls):
        cls.data = cls.open_text()

    # 打开json文件
    @classmethod
    def open_text(cls):

        with open(os.path.abspath('.')+'/Lib/ReagentDB.json', 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
            return content

    # 模糊搜索
    @classmethod
    def search_data(cls, search_word):
        data_list = []
        for drug_dict in cls.data:
            if drug_dict['ChineseName'].find(search_word) != -1 or drug_dict['EnglishName'].find(search_word) != -1:
                new_dict = {}
                new_dict['id'] = drug_dict['CASNumber']
                new_dict['value'] = drug_dict['ChineseName']
                new_dict['subvalue'] = drug_dict['AliasName']
                new_dict['EnglishName'] = drug_dict['EnglishName']
                data_list.append(new_dict)
        # 根据列表的字典的key的长度进行排序
        data_list.sort(key=lambda i: len(i['value']))
        return data_list[:5]


if __name__ == '__main__':
    GetDrugTypeData.init()
    print(GetDrugTypeData().search_data('甲醛'))

