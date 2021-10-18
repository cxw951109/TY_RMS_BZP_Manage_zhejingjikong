from openpyxl import load_workbook
import uuid
import json
import datetime
import time

class ReadExcel:

    def __init__(self, excelName):
        print(3333333333, excelName)
        self.wb = load_workbook(excelName)
        print(self.wb)
        self.ws = self.wb.active
        self.template_list = []

    def read(self):
        max_lines = self.ws.max_row
        print(max_lines)
        if self.ws['C1'].value == 'TemplateContent':
            print(1111111111)
            for key in range(2, max_lines + 1):
                value = self.ws['{}'.format('C' + str(key))].value
                self.template_list.append(value)
            print(self.template_list)
            return self.template_list
        elif self.ws['A1'].value == '申购单编号' and self.ws['B1'].value == '采购单编号':
            drug_list = []
            lineIndex=0
            try:
                print('gggggggggggggggggggggggggggggggggggg')
                for line in range(2, max_lines + 1):
                    lineIndex=line
                    # 声明一个字典存放每一行的数据  每遍历一次字典重置一次
                    drug_template_dict = {}
                    # drug_template_dict['VarietyId'] = str(uuid.uuid1())
                    # drug_template_dict['Name'] = self.ws['A{}'.format(str(line))].value
                    # drug_template_dict['Manufacturer'] = self.ws['B{}'.format(str(line))].value
                    # drug_template_dict['Distributor'] = self.ws['C{}'.format(str(line))].value
                    # drug_template_dict['ProductionDate'] = datetime.datetime.strptime(str(self.ws['D{}'.format(str(line))].value), "%Y/%m/%d %H:%M:%S").strftime("%Y-%m-%d")
                    # drug_template_dict['ShelfLife'] = self.ws['E{}'.format(str(line))].value
                    # drug_template_dict['Price'] = self.ws['F{}'.format(str(line))].value
                    # drug_template_dict['ExportCount'] = self.ws['G{}'.format(str(line))].value
                    # drug_template_dict['Purity'] = self.ws['H{}'.format(str(line))].value
                    # drug_template_dict['CASNumber'] = self.ws['I{}'.format(str(line))].value
                    # drug_template_dict['EnglishName'] = self.ws['J{}'.format(str(line))].value
                    # if self.ws['K{}'.format(str(line))].value != "是":
                    #     drug_template_dict['IsSupervise'] = 0
                    # else:
                    #     drug_template_dict['IsSupervise'] = 1
                    # drug_template_dict['Remark1'] = str(self.ws['L{}'.format(str(line))].value)
                    # drug_template_dict['Remark2'] = str(self.ws['M{}'.format(str(line))].value)
                    # drug_template_dict['Remark3'] = str(self.ws['N{}'.format(str(line))].value)
                    # drug_template_dict['Speci'] = self.ws['O{}'.format(str(line))].value
                    # drug_template_dict['Unit'] = self.ws['P{}'.format(str(line))].value
                    # drug_template_dict['SpeciUnit'] = self.ws['Q{}'.format(str(line))].value
                    drug_template_dict['VarietyId'] = str(uuid.uuid1())
                    drug_template_dict['Remark1'] = str(self.ws['A{}'.format(str(line))].value or '')
                    drug_template_dict['Remark2'] = str(self.ws['B{}'.format(str(line))].value or '')
                    drug_template_dict['Remark3'] = str(self.ws['C{}'.format(str(line))].value or '')
                    drug_template_dict['Remark4'] = str(self.ws['D{}'.format(str(line))].value or '')
                    drug_template_dict['Name'] = str(self.ws['E{}'.format(str(line))].value or '')
                    if(drug_template_dict['Name']==''):
                        self.template_list.append(json.dumps(drug_list))
                        return self.template_list
                    drug_template_dict['EnglishName'] = str(self.ws['F{}'.format(str(line))].value or '')
                    drug_template_dict['Purity'] = str(self.ws['G{}'.format(str(line))].value or '')
                    drug_template_dict['CASNumber'] = str(self.ws['H{}'.format(str(line))].value or '')
                    drug_template_dict['Remark5'] = str(self.ws['I{}'.format(str(line))].value or '')
                    drug_template_dict['Speci'] = str(self.ws['J{}'.format(str(line))].value or '')
                    drug_template_dict['SpeciUnit'] = str(self.ws['K{}'.format(str(line))].value or '')
                    drug_template_dict['ExportCount'] = str(self.ws['L{}'.format(str(line))].value or '')
                    drug_template_dict['Remark6'] = str(self.ws['M{}'.format(str(line))].value or '')
                    if(not self.ws['P{}'.format(str(line))].value and (not self.ws['N{}'.format(str(line))].value or not self.ws['O{}'.format(str(line))].value) ):
                        raise RuntimeError('第{0}行生产日期、保质期或过期日期未按格式填写'.format(str(line)))
                        expirationDate=datetime.datetime.now()+datetime.timedelta(days=365*20)
                        self.ws['P{}'.format(str(line))].value=expirationDate.strftime("%Y-%m-%d %H:%M:%S")
                    if(not self.ws['P{}'.format(str(line))].value):
                        drug_template_dict['ProductionDate'] = datetime.datetime.strptime(str(self.ws['N{}'.format(str(line))].value), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                        drug_template_dict['ShelfLife'] = str(self.ws['O{}'.format(str(line))].value)
                    else:
                        pDate=datetime.datetime.now()
                        if(self.ws['N{}'.format(str(line))].value):
                            pDate= datetime.datetime.strptime(str(self.ws['N{}'.format(str(line))].value), "%Y-%m-%d %H:%M:%S")
                        drug_template_dict['ProductionDate'] =pDate.strftime("%Y-%m-%d")
                        drug_template_dict['ShelfLife'] =self.time_long(datetime.datetime.strptime(pDate.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"),datetime.datetime.strptime(str(self.ws['P{}'.format(str(line))].value), "%Y-%m-%d %H:%M:%S")) 
                    drug_template_dict['Price'] = str(self.ws['Q{}'.format(str(line))].value or '0')
                    if str(self.ws['R{}'.format(str(line))].value) != "是":
                        drug_template_dict['IsSupervise'] = 0
                    else:
                        drug_template_dict['IsSupervise'] = 1
                    drug_template_dict['Remain'] = str(self.ws['S{}'.format(str(line))].value or '0')
                    drug_template_dict['Manufacturer'] = str(self.ws['T{}'.format(str(line))].value or '')
                    drug_template_dict['Remark8'] = str(self.ws['U{}'.format(str(line))].value or '')
                    drug_template_dict['Remark9'] = str(self.ws['V{}'.format(str(line))].value or '')
                    drug_template_dict['Remark10'] = str(self.ws['W{}'.format(str(line))].value or '')
                    drug_list.append(drug_template_dict)

                self.template_list.append(json.dumps(drug_list))
                return self.template_list
            except Exception as e:
                raise RuntimeError('第{0}行;{1}'.format(str(line),str(e)))
        else:
            raise RuntimeError('模板格式错误！')

    def close(self):
        self.wb.close()

    def time_long(self,time1, time2, type="day"):
        """
        计算时间差
        :param time1: 较小的时间（datetime类型）
        :param time2: 较大的时间（datetime类型）
        :param type: 返回结果的时间类型（暂时就是返回相差天数）
        :return: 相差的天数
        """
        day1 = time.strptime(str(time1), '%Y-%m-%d %H:%M:%S')
        day2 = time.strptime(str(time2), '%Y-%m-%d %H:%M:%S')
        if type == 'day':
            day_num = (int(time.mktime(day2)) - int(time.mktime(day1))) / (
                24 * 60 * 60)
        return abs(int(day_num))


if __name__ == '__main__':
    result = ReadExcel('a.xlsx').read()
    print(len(result))
    print(result)
