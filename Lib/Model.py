# 分页参数模型
class PageParam(object):
    def __init__(self, curPage, pageRows, totalRecords=None, orderType=None, orderField=None,):
        self.orderType = orderType  # 排序类型 asc=正序 desc=倒序
        self.orderField = orderField  # 排序字段
        self.pageRows = pageRows  # 单页行数
        self.curPage = curPage  # 当前页码
        self.totalRecords = totalRecords  # 总记录数

    # #获取总页数
    # def getTotalPagesCount(self):
    #     if(self.totalRecords > 0):
    #         return  self.totalRecords % self.pageRows if self.totalRecords % self.pageRows == 0 else self.totalRecords % self.pageRows + 1
    #     else:
    #         return 1

# 试剂操作类型


class DrugRecordType(object):
    # 入库操作
    PutIn = 1

    # 领用操作
    Use = 2

    # 归还操作
    Return = 3

# 试剂状态类型


class DrugStatus(object):
    # 在库
    Normal = 1

    # 出库
    Out = 2

    # 空瓶
    Empty = 3

# 审批类型
class ApproveTypeAllCode(object):
    # 采购审批
    Purchase = 'Purchase'
    # 试剂信息修改审批
    DrugEdit = 'DrugEdit'
    # 试剂信息销毁审批
    DrugDestroy = 'DrugDestroy'

# 审批状态
class ApproveAllStatus(object):
    # 未开始
    NoStart = 1

    # 等待审批
    Waiting = 2

    # 审核通过
    Agree = 3

    # 驳回
    Overrule = 4

