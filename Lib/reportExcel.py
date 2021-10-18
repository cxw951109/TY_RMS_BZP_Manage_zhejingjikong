from openpyxl.workbook import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter
from openpyxl.utils import get_column_letter
import random
from openpyxl.styles import Color, Fill, Font, Alignment, PatternFill, Border, Side
from openpyxl.cell import Cell
import datetime
import string
import json

from Business.BllMedicamentVariety import *
from Business.BllMedicament import *
from Business.BllWarning import *
from Business.BllLog import *
from Business.BllUser import *
from Lib.Utils import Utils


# # 新建一个workbook
# wb = Workbook()
# # 第一个sheet是ws
# ws = wb.worksheets[0]
# # 水平居中, 垂直居中
# alignment_style = Alignment(horizontal='center', vertical='center')
# ws['A1'].font = Font(size=16, bold=True)
# ws['A1'].alignment = alignment_style
# # 设置ws的名称
# ws.title = 'sheet1'
# # 合并单元格 合并第一行的前2列
# x = 1
#
# # 定义Border边框样式
# left, right, top, bottom = [Side(style='thin', color='000000')]*4
# border_style = Border(left=left, right=right, top=top, bottom=bottom)
#
# ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=14)
# ws.cell(row=1, column=1).value = '库存试剂信息概览报表'
#
# # 合并单元格
# while x < 6:
#     ws.merge_cells(start_row=2, end_row=2, start_column=x, end_column=x+1)
#     x += 2
# ws.merge_cells(start_row=2, end_row=2, start_column=7, end_column=14)
#
# # 第2行写入值
# now_time = datetime.datetime.now().strftime('%Y%m%d %H%M')
# # 格式化时间为中文年月日
# now_time = now_time[:4] + '年' + now_time[4:6] + '月' + now_time[6:8] + '日' + now_time[8:11] + '时' + now_time[11:13] + '分'
# ws.cell(row=2, column=1).value = '报表导出时间：{}'.format(now_time)
# ws.cell(row=2, column=3).value = '后台系统版本：Light_OS_Back_ver1.04'
# ws.cell(row=2, column=5).value = '终端系统版本:Light_OS_Front_ver1.06'
# ws.cell(row=2, column=7).value = '报表导出位置：后台'
# # 遍历取1, 3, 5, 7为第二行添加样式
# for x in range(1, 8, 2):
#     ws.cell(row=2, column=x).font = Font(size=9)
#     # 水平对齐 垂直对齐
#     ws.cell(row=2, column=x).alignment = alignment_style
#     if x < 7:
#         # 边框样式
#         ws.cell(row=2, column=x).border = border_style
#         ws.cell(row=2, column=x + 1).border = border_style
#     else:
#         # 因为第2行第7-14列是合并的单元格 所以需要循环添加边框样式
#         while x < 15:
#             ws.cell(row=2, column=x).border = border_style
#             x += 1
#
#
# # 第三行的值
# data_list = ['试剂类别', '纯度', 'CAS码', '重点监管', '当前库存总量', '当前在库数量', '当前借出数量', '库存价值(元)',
#            '季度历史库存总量', '季度消耗总量', '季度消耗价值', '年度历史存库量', '年度消耗总量', '年度消耗价值']
#
# for data in range(1, len(data_list) + 1):
#     # 第三行写入值
#     ws.cell(row=3, column=data).value = data_list[data - 1]
#     # 设置文本水平居中, 垂直居中
#     ws.cell(row=3, column=data).alignment = alignment_style
#     #  设置字体加粗
#     ws.cell(row=3, column=data).font = Font(bold=True, size=9)
#     # 背景颜色
#     ws.cell(row=3, column=data).fill = PatternFill(fill_type='solid', fgColor='EE9A49')
#     # 边框样式
#     ws.cell(row=3, column=data).border = border_style
#
# # 设置行高
# ws.row_dimensions[1].height = 35
# ws.row_dimensions[2].height = 25
# ws.row_dimensions[3].height = 28
# ws.row_dimensions[4].height = 18
# for data in range(1, len(data_list) + 1):
#     ws.cell(row=4, column=data).value = random.randint(1, 20)
#     # 设置文本水平居中, 垂直居中
#     ws.cell(row=4, column=data).alignment = alignment_style
#     # 设置边框样式
#     ws.cell(row=4, column=data).border = border_style
#     # 设置字体大小
#     ws.cell(row=4, column=data).font = Font(size=9)
#
#
#
# wb.save('库存试剂信息概览报表{}.xlsx'.format(random.randint(1, 20)))









# alignment = Alignment(
#     horizontal = 'general', # 水平：常规
#     vertical = 'bottom',   # 垂直：底部对齐
#     text_rotation = 0,   # 文本方向：0度
#     wrap_text = False,   # 自动换行
#     shrink_to_fit = False,  # 缩小字体填充
#     indent = 0 # 缩进0
#   )


class ReportData:

    def __init__(self):
        # 新建一个workbook
        self.wb = Workbook()
        # 定义设置样式
        self.a = 0

    def set_style(self, title='sheet1'):
        # 如果是第一次调用则删除默认创建的sheet表
        if self.a == 0:
            self.wb.remove(self.wb['Sheet'])
            self.a += 1
        # 创建sheet
        self.ws = self.wb.create_sheet()
        # 设置sheet的标题
        self.ws.title = title
        # 设置1 2 3 行固定的高度
        self.ws.row_dimensions[1].height = 35
        self.ws.row_dimensions[2].height = 25
        self.ws.row_dimensions[3].height = 28
        # 水平对齐, 居中对齐
        self.alignment_style = Alignment(horizontal='center', vertical='center')
        # 定义Border边框样式
        left, right, top, bottom = [Side(style='thin', color='000000')] * 4
        self.border_style = Border(left=left, right=right, top=top, bottom=bottom)
        # 设置列宽
        # 生成前14个大写字母  ascii_uppercase生成所有大写字母
        self.upper_string = string.ascii_uppercase[:15]
        # 定义字体
        self.font_size = Font(size=9)
        for col in self.upper_string:
            self.ws.column_dimensions[col].width = 20

    # 创建第一行
    def create_row1(self, value, length):
        # 合并第1行1-14列单元格
        self.ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=length)
        # 写入值
        self.ws.cell(row=1, column=1).value = value
        self.ws['A1'].alignment = self.alignment_style
        self.ws['A1'].font = Font(size=16, bold=True)
        self.create_row2(length)

    def create_row2(self, length):
        # 第2行写入值
        now_time = datetime.datetime.now().strftime('%Y%m%d %H%M')
        # 格式化时间为中文年月日
        now_time = now_time[:4] + '年' + now_time[4:6] + '月' + now_time[6:8] + '日' + now_time[8:11] + '时' + now_time[11:13] + '分'
        self.ws.cell(row=2, column=1).value = '报表导出时间：{}'.format(now_time)
        self.ws.cell(row=2, column=3).value = '后台系统版本：Light_OS_Back_ver1.04'
        self.ws.cell(row=2, column=5).value = '终端系统版本:Light_OS_Front_ver1.06'
        self.ws.cell(row=2, column=7).value = '报表导出位置：后台'
        # 合并单元格
        x = 1
        while x < 6:
            self.ws.merge_cells(start_row=2, end_row=2, start_column=x, end_column=x+1)
            x += 2
        if length > 7:
            self.ws.merge_cells(start_row=2, end_row=2, start_column=7, end_column=length)
        # 遍历取1, 3, 5, 7为第二行添加样式
        for x in range(1, 8, 2):
            self.ws.cell(row=2, column=x).font = Font(size=9)
            # 水平对齐 垂直对齐
            self.ws.cell(row=2, column=x).alignment = self.alignment_style
            if x < 7:
                # 边框样式
                self.ws.cell(row=2, column=x).border = self.border_style
                self.ws.cell(row=2, column=x + 1).border = self.border_style
            else:
                # 因为第2行第7-14列是合并的单元格 所以需要循环添加边框样式
                while x < length+1:
                    self.ws.cell(row=2, column=x).border = self.border_style
                    x += 1

    # 创建第三行, 需要传入一个列表用来写入单元格的值
    def create_row3(self, data_list):
        for data in range(1, len(data_list) + 1):
            # 第三行写入值
            self.ws.cell(row=3, column=data).value = data_list[data - 1]
            # 设置文本水平居中, 垂直居中
            self.ws.cell(row=3, column=data).alignment = self.alignment_style
            #  设置字体加粗
            self.ws.cell(row=3, column=data).font = Font(bold=True, size=9)
            # 背景颜色
            self.ws.cell(row=3, column=data).fill = PatternFill(fill_type='solid', fgColor='EE9A49')
            # 边框样式
            self.ws.cell(row=3, column=data).border = self.border_style

    # 创建多行固定样式 start_row从第几行开始有规律 传入一个数据库获取的列表对象的值, 传入一个数据对象keys列表
    def create_multiple_rows(self, start_row, data_list, keys_list):
        # 从第4行创建
        for row_number in range(start_row, len(data_list) + start_row):
            # 设置每一行的行高
            self.ws.row_dimensions[row_number].height = 18
            # 遍历每一个对象的长度
            col_ = 1
            for key_ in keys_list:
                # 写入值
                self.ws.cell(row=row_number, column=col_).value = data_list[row_number-start_row][key_]
                # 设置文本水平居中, 垂直居中
                self.ws.cell(row=row_number, column=col_).alignment = self.alignment_style
                # 设置边框样式
                self.ws.cell(row=row_number, column=col_).border = self.border_style
                # 设置字体大小
                self.ws.cell(row=row_number, column=col_).font = Font(size=9)
                col_ += 1

    # 保存文件
    def save(self, file_path):
        self.wb.save('{}.xlsx'.format(file_path))
        self.close()

    # 关闭文件
    def close(self):
        self.wb.close()

    # 替换空白
    def replace_space(self, length):
        self.max_lines = self.ws.max_row
        upper_letter_str = string.ascii_uppercase[:length]
        for upper_letter in upper_letter_str:
            for row_ in range(1, self.max_lines+1):
                b = self.ws[upper_letter + str(row_)].value
                if b == None or b == '':
                    self.ws[upper_letter + str(row_)].value = 'null'

    # 编辑excel表格中列试剂状态1 2 3 替换为在库 出库 空瓶
    def editor_status(self, col_):
        self.max_lines = self.ws.max_row
        for row_ in range(4, self.max_lines+1):
            b = self.ws[col_ + str(row_)].value
            if b == 1:
                self.ws[col_ + str(row_)].value = '在库'
            elif b == 2:
                self.ws[col_ + str(row_)].value = '出库'
            elif b == 3:
                self.ws[col_ + str(row_)].value = '空瓶'
            elif b == 5:
                self.ws[col_ + str(row_)].value = '预备入库'

    # 编辑试剂重点监管列为1 0 替换为是 否
    def editor_isSupervise(self, col_):
        self.max_lines = self.ws.max_row
        for row_ in range(4, self.max_lines+1):
            b = self.ws[col_ + str(row_)].value
            if b == 1:
                self.ws[col_ + str(row_)].value = '是'
            elif b == 0:
                self.ws[col_ + str(row_)].value = '否'

    # 编辑用户管理列为1 0 替换为正常 禁用
    def editor_user_status(self, col_):
        self.max_lines = self.ws.max_row
        for row_ in range(4, self.max_lines + 1):
            b = self.ws[col_ + str(row_)].value
            if b == 1:
                self.ws[col_ + str(row_)].value = '正常'
            elif b == 0:
                self.ws[col_ + str(row_)].value = '禁用'

    # 编辑操作类型 1 2 3 入库 领用 归还
    def editor_RecordType(self, col_):
        self.max_lines = self.ws.max_row
        for row_ in range(4, self.max_lines + 1):
            b = self.ws[col_ + str(row_)].value
            if b == 1:
                self.ws[col_ + str(row_)].value = '入库'
            elif b == 2:
                self.ws[col_ + str(row_)].value = '领用'
            elif b == 3:
                self.ws[col_ + str(row_)].value = '归还'

    # 替换sqlAlchemy时间格式
    def editor_time(self, keys_list, params):
        self.max_lines = self.ws.max_row
        for row_ in range(4, self.max_lines + 1):
            col_ = string.ascii_uppercase[keys_list.index(params)]
            b = self.ws[col_ + str(row_)].value
            if len(b) == 19:
                self.ws[col_ + str(row_)].value = b.replace('T', ' ')

    # 下载文件
    @staticmethod
    def download_excel(filename, chunk_size=512):
        try:
            f = open(filename, 'rb')
        except Exception as e:
            logger.debug('读取文件异常'+str(e))
            return
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                f.close()
                os.remove(filename)
                break


if __name__ == '__main__':
    pass
