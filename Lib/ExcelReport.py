import openpyxl
from openpyxl import Workbook
from openpyxl.drawing import image
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, colors

"""试验报表类"""

class ExcelReport(object):
    def __init__(self, data, path):
        self.data = data
        self.path = path
        cells = ['A', 'B', 'C', 'D', 'E', 'F']
        # 工作簿实例化
        wb = Workbook()
        self.book = wb
        # 激活工作表
        ws = wb.active
        #ws1 = wb.create_sheet("Mysheet")
        # 更改表名
        ws.title = "流出杯实验报表"

        for cell in cells:
            ws.column_dimensions[cell].width = 20
        sideStyle = Side(border_style='thin', color='00000000')
        borderStyle = Border(left=sideStyle, right=sideStyle,
                             top=sideStyle, bottom=sideStyle)

        # 第1行
        ws.row_dimensions[1].height = 35
        ws.merge_cells('A1:F1')
        ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
        ws['A1'].font = Font(name='宋体', size=20, bold=True)

        for x in ws['A1:F1']:
            for y in x:
                y.border = borderStyle
        ws['A1'] = "自动流出杯式粘度测定仪试验报表"

        # 第2行
        ws.merge_cells('A2:F2')
        ws.row_dimensions[2].height = 20
        ws['A2'].alignment = Alignment(horizontal='left', vertical='center')
        ws['A2'].font = Font(name='宋体', size=13, bold=True)
        ws['A2'] = "实验基本信息"
        for x in ws['A2:F2']:
            for y in x:
                y.border = borderStyle

        # 第3行
        ws.merge_cells('A3:B3')
        ws.merge_cells('C3:D3')
        ws.merge_cells('E3:F3')
        ws.row_dimensions[3].height = 25
        for x in ws['A3:F3']:
            for y in x:
                y.border = borderStyle
                y.font = Font(name='宋体', size=12)
                y.alignment = Alignment(horizontal='center', vertical='center')
        ws['A3'] = "实验时间：" + data[0].start_time
        ws['C3'] = "试验类型：" + self.getExperimentTypeName(data[0].experiment_type)
        ws['E3'] = "实验人：" + data[0].experiment_user_name

        # 第4行
        ws.merge_cells('A4:B4')
        ws.merge_cells('C4:D4')
        ws.merge_cells('E4:F4')
        ws.row_dimensions[4].height = 25
        for x in ws['A4:F4']:
            for y in x:
                y.border = borderStyle
                y.font = Font(name='宋体', size=12)
                y.alignment = Alignment(horizontal='center', vertical='center')
        ws['A4'] = "试验材料：" + data[0].material_name
        ws['C4'] = "流出杯规格：{0}号杯".format(data[0].cup_type)
        ws['E4'] = "结论：" + str(data[0].result)

        # 第5行
        ws.merge_cells('A5:B5')
        ws.merge_cells('C5:D5')
        ws.merge_cells('E5:F5')
        ws.row_dimensions[5].height = 25
        for x in ws['A5:F5']:
            for y in x:
                y.border = borderStyle
                y.font = Font(name='宋体', size=12)
                y.alignment = Alignment(horizontal='center', vertical='center')
        ws['A5'] = "试验次数：" + str(data[0].total_count)
        ws['C5'] = "总耗时：{0}s".format(data[0].total_cost/10)
        ws['E5'] = "平均耗时：{0}s".format(data[0].total_cost / data[0].total_count/10)

        # 第6行
        ws.merge_cells('A6:F6')
        ws.row_dimensions[6].height = 20
        ws['A6'].alignment = Alignment(horizontal='left', vertical='center')
        ws['A6'].font = Font(name='宋体', size=13, bold=True)
        ws['A6'] = "实验阶段耗时信息"
        for x in ws['A6:F6']:
            for y in x:
                y.border = borderStyle

        # 第8行
        ws.merge_cells('A8:F8')
        ws.row_dimensions[8].height = 20
        ws['A8'].alignment = Alignment(horizontal='left', vertical='center')
        ws['A8'].font = Font(name='宋体', size=13, bold=True)
        ws['A8'] = "实验温度信息"
        for x in ws['A8:F8']:
            for y in x:
                y.border = borderStyle
        # 第9行
        ws.merge_cells('A9:B9')
        ws.merge_cells('C9:D9')
        ws.merge_cells('E9:F9')
        ws.row_dimensions[9].height = 25
        for x in ws['A9:F9']:
            for y in x:
                y.border = borderStyle
                y.font = Font(name='宋体', size=12)
                y.alignment = Alignment(horizontal='center', vertical='center')
        # 第10行
        ws.row_dimensions[10].height = 25
        for x in ws['A10:F10']:
            for y in x:
                y.border = borderStyle
                y.font = Font(name='宋体', size=12)
                y.alignment = Alignment(horizontal='center', vertical='center')

        ws.merge_cells('A7:B7')
        ws.merge_cells('C7:D7')
        ws.merge_cells('E7:F7')
        ws.row_dimensions[7].height = 25
        for x in ws['A7:F7']:
            for y in x:
                y.border = borderStyle
                y.font = Font(name='宋体', size=12)
                y.alignment = Alignment(horizontal='center', vertical='center')



        lenghtlist = []
        for index, x in enumerate(data[1]):
            lenghtlist.append(len(data[2][index]))
            ws[cells[index * 2] + '7'] = "试样{0}实验耗时：{1}s".format(index + 1, x.time_cost/10)
            ws[cells[index * 2] + '9'] = "试样{0}实验温度".format(index + 1)
            ws[cells[index * 2] + '10'] = "记录时间"
            ws[cells[index * 2 + 1] + '10'] = "温度值"
            for index1, x1 in enumerate(data[2][index]):
                ws.row_dimensions[index1 + 11].height = 18
                ws[cells[index * 2] + str(index1 + 11)] = x1.record_time
                ws[cells[index * 2 + 1] + str(index1 + 11)] = x1.temp_value

        for x in ws['A11:F' + str(max(lenghtlist) + 10)]:
            for y in x:
                y.border = borderStyle
                y.font = Font(name='宋体', size=12)
                y.alignment = Alignment(horizontal='center', vertical='center')

        rowIndex = max(lenghtlist) + 11
        ws.row_dimensions[rowIndex].height = 20
        ws.merge_cells('A{0}:F{1}'.format(str(rowIndex),str(rowIndex)))
        ws['A' + str(rowIndex)].alignment = Alignment(horizontal='left', vertical='center')
        ws['A' + str(rowIndex)].font = Font(name='宋体', size=13, bold=True)
        ws['A' + str(rowIndex)] = "实验断点图片"
        for x in ws['A{0}:F{1}'.format(str(rowIndex),str(rowIndex))]:
            for y in x:
                y.border = borderStyle

        rowIndex+=1
        ws.row_dimensions[rowIndex].height = 25
        ws.merge_cells('A{0}:B{1}'.format(str(rowIndex),str(rowIndex)))
        ws.merge_cells('C{0}:D{1}'.format(str(rowIndex),str(rowIndex)))
        ws.merge_cells('E{0}:F{1}'.format(str(rowIndex),str(rowIndex)))
        for x in ws['A{0}:F{1}'.format(str(rowIndex),str(rowIndex))]:
            for y in x:
                y.border = borderStyle
                y.alignment = Alignment(horizontal='center', vertical='center')
                y.font = Font(name='宋体', size=12)

        rowIndex+=1
        ws.row_dimensions[rowIndex].height = 400
        ws.merge_cells('A{0}:B{1}'.format(str(rowIndex),str(rowIndex)))
        ws.merge_cells('C{0}:D{1}'.format(str(rowIndex),str(rowIndex)))
        ws.merge_cells('E{0}:F{1}'.format(str(rowIndex),str(rowIndex)))
        ws['A' + str(rowIndex)].alignment = Alignment(horizontal='center', vertical='center')
        ws['A' + str(rowIndex)].font = Font(name='宋体', size=12)
        #ws.add_image(image.Image("/home/pi/Downloads/11/Resources/EXImages/{0}/1.jpg".format(data[0].experiment_id)),
        #'A' + rowIndex)
        #ws.add_image(image.Image("/home/pi/Downloads/11/Resources/EXImages/{0}/2.jpg".format(data[0].experiment_id)),
        #'C' + rowIndex)
        #ws.add_image(image.Image("/home/pi/Downloads/11/Resources/EXImages/{0}/3.jpg".format(data[0].experiment_id)),
        #'E' + rowIndex)
        for x in ws['A{0}:F{1}'.format(str(rowIndex),str(rowIndex))]:
            for y in x:
                y.border = borderStyle

        for index, x in enumerate(data[1]):
            ws[cells[index * 2] + str(rowIndex - 1)] = "试样{0}断点图片".format(index + 1)
            #img =
            #image.Image("/home/pi/Downloads/11/Resources/EXImages/{0}/1.jpg".format(data[0].experiment_id))
            #img.anchor(ws.cell("{0}{1}".format(cells[index * 2],rowIndex)))
            #ws.add_image(img)
            ws.add_image(image.Image("/home/pi/Downloads/11/Resources/EXImages/{0}/{1}.jpg".format(data[0].experiment_id,index + 1)),"{0}{1}".format(cells[index * 2],rowIndex))
        ws.add_image(image.Image("image.png"),"A{0}".format(rowIndex+12))

    # 导出
    def export(self):
        try:
            self.book.save(self.path)
        except Exception as e:
            print(e)

    def getExperimentTypeName(self,experimentType):
        if(experimentType==1):
            return '标准试验'
        elif(experimentType==2):
            return '预备试验'
        elif(experimentType==3):
            return '校准试验'
        else:
            return '标准试验'



if __name__ == "__main__":
    import ExcelReport
    excelReport = ExcelReport.ExcelReport(BllExperiment().getExperimentAllInfo('067a5926-3dce-11e8-a46a-b827eb9007d3'), "22222.xls")
    excelReport.export()
