from datetime import date
from datetime import datetime
from dateutil import relativedelta
import json
import random
import string
import os

from django.shortcuts import render
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.http import urlquote

from Business.BllMedicament import *
from Business.BllClient import *
from Business.BllWarning import *
from Business.BllUser import *
from Lib.reportExcel import *
from Lib.Utils import *


@require_http_methods(['GET'])
def index(request):
    if request.method == 'GET':
        return render(request, 'dataReport/index.html', locals())


# 获取试剂记录返回页面
@require_http_methods(['GET'])
def drugRecordList(request):
    if request.method == 'GET':
        endDate = (date.today() + relativedelta.relativedelta(days=1)).strftime('%Y-%m-%d')
        startDate = (date.today() + relativedelta.relativedelta(years=-1, days=1)).strftime('%Y-%m-%d')
        return render(request, 'dataReport/drugRecordList.html', locals())


@require_http_methods(['GET'])
def drugShelfLifeList(request):
    if request.method == 'GET':
        return render(request, 'dataReport/drugShelfLifeList.html', locals())


@require_http_methods(['GET'])
def categoryCountList(request):
    if request.method == 'GET':
        return render(request, 'dataReport/categoryCountList.html', locals())


@require_http_methods(['GET'])
def userList(request):
    if request.method == 'GET':
        return render(request, 'dataReport/userList.html', locals())


@require_http_methods(['GET'])
def warningList(request):
    if request.method == 'GET':
        return render(request, 'dataReport/warningList.html', locals())


# 获取客户端数量
@require_http_methods(['GET'])
def getClientListJson(request):
    if request.method == 'GET':
        client_list = BllClient().getAllClientList()
        print('mxh_客户端类型是', json.loads(Utils.resultAlchemyData(client_list)))
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(client_list))})


# 获取操作类型
@require_http_methods(['GET'])
def getRecordType(request):
    if request.method == 'GET':
        SQL = "SELECT distinct RecordType FROM RMS_MedicamentRecord ORDER BY RecordType asc"
        report_record_type = BllMedicamentRecord().execute(SQL).fetchall()
        print('mxh_操作类型是', report_record_type)
        print(json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(report_record_type))))
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.
                                                                        mysqlTable2Model(report_record_type)))})


# 获取药品流转记录数据
@require_http_methods(['GET'])
def getDrugRecordListJson(request):
    if request.method == 'GET':
        client_id = request.GET.get('client_id', '')
        search_val = request.GET.get('search_val', '')
        startDate = request.GET.get('startDate', '')
        endDate = request.GET.get('endDate', '')
        recordtype_val = request.GET.get('recordtype_val', '')
        str1 = ""
        print('传递前',client_id, search_val, startDate, endDate, recordtype_val)
        # mxh_获取条件查询到的数据
        report_record_list = DrugUseRecordInfoSelect(client_id, search_val, startDate, endDate, recordtype_val)
        return JsonResponse({'data':report_record_list})


# 试剂记录图表页面
@require_http_methods(['GET'])
def drugRecordChart(request):
    if request.method == 'GET':
        current_year = date.today().strftime('%Y')
        # 获得近三年的年份
        nearly_three_year = []
        for x in range(3):
            nearly_three_year.append(int(current_year) - x)
        return render(request, 'dataReport/drugRecordChart.html', locals())


# 获取试剂流转记录
@require_http_methods(['GET'])
def getDrugRecordChartJson(request):
    if request.method == 'GET':
        # 获取当前选择年份
        year = request.GET.get('year')
        SQL = """
        SELECT a.CreateDate, sum( CASE when a.RecordType = 1 then 1 else 0 end) as 'putInCountList', 
        sum( CASE when a.RecordType = 2 then 1 else 0 end) as 'useCountList', 
        sum( CASE when a.RecordType = 3 then 1 else 0 end) as 'returnCountList' from RMS_MedicamentRecord 
            as a WHERE DATE_FORMAT(a.CreateDate, '%Y') = :year GROUP by DATE_FORMAT(a.CreateDate, '%Y-%m')
        """
        # 当前月份
        now_month = datetime.datetime.now().strftime('%m')
        # 当前年份
        current_year = datetime.datetime.now().strftime('%Y')
        # 获取数据库入库, 借出, 归还数据
        HumitureRecord_obj_list = BllHumitureRecord().execute(SQL, {'year': year}).fetchall()
        # 把列表对象转化成列表字典类型
        HumitureRecord_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(HumitureRecord_obj_list)))
        # 入库
        putInCountList = []
        # 借出
        useCountList = []
        # 归还
        returnCountList = []
        # 月份列表
        month_list = []

        if year == current_year:
            now_month = int(now_month)
        else:
            now_month = 12

        for x in range(now_month):
            # 当月份小于10 格式化为0x月格式 x是从0开始所有应该是小于9
            if x < 9:
                x = '0' + str(x + 1)
            else:
                x += 1
            for HumitureRecord_obj in HumitureRecord_obj_list:
                # 判断当前遍历月份是否等于数据库存在的月份, 如果等于就给得到的值, 否则增加0
                if HumitureRecord_obj['CreateDate'][5:7] == str(x):
                    putInCountList.append(int(HumitureRecord_obj['putInCountList']))
                    useCountList.append(int(HumitureRecord_obj['useCountList']))
                    returnCountList.append(int(HumitureRecord_obj['returnCountList']))
                    # 有就跳出循环
                    break
            else:
                # 如果正常循环, 则代表数据库没有此月份, 就增加数值0
                putInCountList.append(0)
                useCountList.append(0)
                returnCountList.append(0)
            month_list.append(str(x) + '月')

        # 返回前段展示的data数据
        data = {"xAxisList": month_list, "putInCountList": putInCountList, "useCountList": useCountList,
                "returnCountList": returnCountList}

        return JsonResponse({'data': data})


# 获取库存记录类别Json数据
def getCategoryCountListJson(request):
    if request.method == 'GET':
        SQL = """
                        SELECT  b.VarietyId as VarietyId, COUNT(CASE when IsEmpty = 1 then 1 end) as QuarterlyEmptyCount, 
                              sum(CASE when IsEmpty = 1 then a.price else 0 end) as QuarterlyEmptyPrice, COUNT(CASE when RecordType = 1 then 1 end) as 
                              QuarterlyPutInCount from RMS_MedicamentVariety  as b LEFT JOIN RMS_MedicamentRecord as a on
                               b.VarietyId = a.VarietyId and QUARTER((a.CreateDate)) = QUARTER(now()) and Date_format
                              (a.CreateDate, '%Y') = (DATE_FORMAT(now(), '%Y')) GROUP by b.VarietyId
                        """
        # 获取季度数据
        quarter_data = BllMedicamentVariety().execute(SQL).fetchall()
        quarter_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(quarter_data)))
        SQL = """SELECT  b.VarietyId as VarietyId, COUNT(CASE when IsEmpty = 1 then a.CreateDate end) 
                              as YearEmptyCount, sum(CASE when IsEmpty = 1 then a.price else 0 end) as YearEmptyPrice,
                              COUNT(CASE when RecordType = 1 then 1 end) as YearPutInCount from RMS_MedicamentVariety  as b LEFT JOIN 
                              RMS_MedicamentRecord as a on b.VarietyId = a.VarietyId and year((a.CreateDate)) = 
                              year(now()) GROUP by b.VarietyId"""

        # 获取年度数据
        year_data = BllMedicamentVariety().session.execute(SQL).fetchall()
        year_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(year_data)))
        SQL = """
            select  a.VarietyId as VarietyId, a.Name,a.Purity,a.CASNumber,a.IsSupervise, 
            sum(case when b.`Status` = 1 then 1 else 0 end) as NormalCount,  
            sum(case when b.`Status` = 1 or b.`Status` = 2 then 1 else 0 end) as TotalCount,
            sum(case when b.`Status` = 2 then 1 else 0 end) as UseCount, 
            sum(case when b.`Status` = 1 or b.`Status` = 2 then b.Price else 0 end)  as StockPrice 
            from RMS_MedicamentVariety as a LEFT JOIN RMS_Medicament
            as b on b.VarietyId = a.VarietyId GROUP BY a.VarietyId
        """
        # 获取试剂数据
        med_data = BllMedicamentVariety().execute(SQL).fetchall()
        med_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(med_data)))
        data_list = []
        new_data_list = []
        # 便利数据合通过VarietyId相同合并字典
        for quarter in quarter_data:
            for year in year_data:
                if quarter['VarietyId'] == year['VarietyId']:
                    new_data = dict(quarter, **year)
                    data_list.append(new_data)
        for data_dict in data_list:
            for med in med_data:
                if data_dict['VarietyId'] == med['VarietyId']:
                    new_data = dict(data_dict, **med)
                    new_data_list.append(new_data)
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(new_data_list))})


# 获取预警列表Json数据
def getWarningListJson(request):
    if request.method == 'GET':
        warning_list = BllWarning().findList().all()
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(warning_list))})


# 获取试剂列表Json数据
@require_http_methods(['GET'])
def getDrugListJson(request):
    if request.method == 'GET':
        client_id = request.GET.get('ClientId', '')
        if not client_id:
            try:
                SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament;"
                drug_obj_list = BllMedicament().execute(SQL).fetchall()
                return JsonResponse(
                    {'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})
            except:
                logger.debug('数据库操作失败')
                BllMedicament().session.rollback()
        else:
            try:
                SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament where " \
                      "RMS_Medicament.ClientId = :client_id;"
                drug_obj_list = BllMedicament().execute(SQL, {'client_id': client_id}).fetchall()
                return JsonResponse(
                    {'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})
            except:
                logger.debug('数据库操作失败')
                BllMedicament().session.rollback()
                drug_obj_list = []
                return JsonResponse(
                    {'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})


# 试剂保质期统计图
@require_http_methods(['GET'])
def drugShelfLifeChart(request):
    if request.method == 'GET':
        return render(request, 'dataReport/drugShelfLifeChart.html', locals())


@require_http_methods(['GET'])
def getDrugShelfLifeChartJson(request):
    if request.method == 'GET':
        SQL = "SELECT count(CASE when TO_DAYS(ExpirationDate) - TO_DAYS(now()) BETWEEN  0 and 5 then '符合'" \
              " end) as '离过期小于5天',count(CASE when TO_DAYS(ExpirationDate) - TO_DAYS(now()) BETWEEN " \
              " 6 and 30 then '符合' end) as '离过期5-30天'," \
              "count(CASE when TO_DAYS(ExpirationDate) - TO_DAYS(now()) BETWEEN  31 and 180 then '符合' end)" \
              " as '离过期30-180天', count(CASE when TO_DAYS(ExpirationDate) - TO_DAYS(now()) BETWEEN  181 " \
              "and 360 then '符合' end) as '离过期180-360天',count(CASE when TO_DAYS(ExpirationDate) - " \
              "TO_DAYS(now()) > 360 then '符合' end) as '离过期大于360天'from RMS_Medicament"
        # 获取数据
        Medicament_ExpirationDate_data = BllMedicament().execute(SQL).fetchall()
        # 转化成明文列表数据
        ex_data_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(Medicament_ExpirationDate_data)))
        new_data_list = []
        key_list = []
        # 遍历插入数据
        for ex_data_dict in ex_data_list:
            for k, v in ex_data_dict.items():
                key_list.append(k)
                new_data_list.append({'name': k, 'value': v})
        data = {
            'legend': key_list,
            "data": new_data_list
        }
        return JsonResponse({'data': data})


def fundsConsumeChart(request):
    if request.method == 'GET':
        last_year = (datetime.datetime.now() + relativedelta.relativedelta(years=-1)).strftime('%Y')
        last_last_year = (datetime.datetime.now() + relativedelta.relativedelta(years=-2)).strftime('%Y')
        return render(request, 'dataReport/FundsConsumeChart.html', locals())


@require_http_methods(['GET'])
def getFundsConsumeChartJson(request):
    if request.method == 'GET':
        year = request.GET.get('year', '')
        month = request.GET.get('month', '')
        if year and month == '0':
            # 获取年度总消耗资金如果为null 则用0 代替
            SQL = """SELECT  Name, Purity, b.VarietyId as VarietyId, (case WHEN (sum(CASE when IsEmpty = 1 
                    then a.price end)) is Null  then 0 else sum(CASE when IsEmpty = 1 then a.price end) end) as 
                    YearEmptyPrice from RMS_MedicamentVariety  as b LEFT JOIN RMS_MedicamentRecord as a 
                    on b.VarietyId = a.VarietyId and year((a.CreateDate)) = :year GROUP by 
                    b.VarietyId order by YearEmptyPrice desc;"""
            YearEmptyPrice_data_list = BllMedicamentVariety().execute(SQL, {'year': year})
            YearEmptyPrice_data_list = json.loads(
                Utils.resultAlchemyData(Utils.mysqlTable2Model(YearEmptyPrice_data_list)))

            new_data_list = []
            name_list = []
            for YearEmptyPrice_data_obj in YearEmptyPrice_data_list[:4]:
                name_list.append(YearEmptyPrice_data_obj['Name'] + YearEmptyPrice_data_obj['Purity'])
                new_data_list.append({'value': YearEmptyPrice_data_obj['YearEmptyPrice'],
                                      'name': YearEmptyPrice_data_obj['Name'] + YearEmptyPrice_data_obj['Purity']})
            sum_else_value = 0
            for YearEmptyPrice_data_obj in YearEmptyPrice_data_list[4:]:
                sum_else_value += float(YearEmptyPrice_data_obj['YearEmptyPrice'])
            name_list.append('其他')
            new_data_list.append({'value': sum_else_value, 'name': '其他'})

            data = {"legend": name_list,
                    "data": new_data_list}
            return JsonResponse({'data': data})


# 获取在库价值页面
@require_http_methods(['GET'])
def fundsNormalChart(request):
    if request.method == 'GET':
        return render(request, 'dataReport/fundsNormalChart.html', locals())


# 获取在库价值Json数据
@require_http_methods(['GET'])
def getFundsNormalChartJson(request):
    if request.method == 'GET':
        SQL = """select  a.VarietyId as VarietyId, a.Name,a.Purity, 
        sum(case when b.`Status` = 1 or b.`Status` = 2 then b.Price else 0 end)  as StockPrice 
        from RMS_MedicamentVariety as a LEFT JOIN RMS_Medicament
              as b on b.VarietyId = a.VarietyId GROUP BY a.VarietyId """
        StockPrice_data_list = BllMedicamentVariety().execute(SQL)
        StockPrice_data_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(StockPrice_data_list)))

        new_data_list = []
        name_list = []
        for YStockPrice_data_list_data_obj in StockPrice_data_list[:4]:
            name_list.append(YStockPrice_data_list_data_obj['Name'] + YStockPrice_data_list_data_obj['Purity'])
            new_data_list.append({'value': YStockPrice_data_list_data_obj['StockPrice'],
                                  'name': YStockPrice_data_list_data_obj['Name'] + YStockPrice_data_list_data_obj[
                                      'Purity']})
        sum_else_value = 0
        for YStockPrice_data_list_data_obj in StockPrice_data_list[4:]:
            if YStockPrice_data_list_data_obj['StockPrice'] is not None:
                sum_else_value += float(YStockPrice_data_list_data_obj['StockPrice'])
        name_list.append('其他')
        new_data_list.append({'value': sum_else_value, 'name': '其他'})

        data = {"legend": name_list,
                "data": new_data_list}
        return JsonResponse({'data': data})


# 导出库存试剂信息报表
@require_http_methods(['GET'])
def ExportDrugCategoryData(request):
    if request.method == 'GET':
        SQL = """
                SELECT  b.VarietyId as VarietyId, COUNT(CASE when IsEmpty = 1 then 1 end) as QuarterlyEmptyCount, 
                      sum(CASE when IsEmpty = 1 then a.price else 0 end) as QuarterlyEmptyPrice, COUNT(CASE when RecordType = 1 then 1 end) as 
                      QuarterlyPutInCount from RMS_MedicamentVariety  as b LEFT JOIN RMS_MedicamentRecord as a on
                       b.VarietyId = a.VarietyId and QUARTER((a.CreateDate)) = QUARTER(now()) and Date_format
                      (a.CreateDate, '%Y') = (DATE_FORMAT(now(), '%Y')) GROUP by b.VarietyId
                """
        # 获取季度数据
        quarter_data = BllMedicamentVariety().execute(SQL).fetchall()
        quarter_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(quarter_data)))
        SQL = """SELECT  b.VarietyId as VarietyId, COUNT(CASE when IsEmpty = 1 then a.CreateDate end) 
                      as YearEmptyCount, sum(CASE when IsEmpty = 1 then a.price else 0 end) as YearEmptyPrice,
                      COUNT(CASE when RecordType = 1 then 1 end) as YearPutInCount from RMS_MedicamentVariety  as b LEFT JOIN 
                      RMS_MedicamentRecord as a on b.VarietyId = a.VarietyId and year((a.CreateDate)) = 
                      year(now()) GROUP by b.VarietyId"""

        # 获取年度数据
        year_data = BllMedicamentVariety().session.execute(SQL).fetchall()
        year_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(year_data)))
        SQL = """
                   select  a.VarietyId as VarietyId, a.Name,a.Purity,a.CASNumber,a.IsSupervise, 
                   sum(case when b.`Status` = 1 then 1 else 0 end) as NormalCount,  
                   sum(case when b.`Status` = 1 or b.`Status` = 2 then 1 else 0 end) as TotalCount,
                   sum(case when b.`Status` = 2 then 1 else 0 end) as UseCount, 
                   sum(case when b.`Status` = 1 or b.`Status` = 2 then b.Price else 0 end)  as StockPrice 
                   from RMS_MedicamentVariety as a LEFT JOIN RMS_Medicament
                   as b on b.VarietyId = a.VarietyId GROUP BY a.VarietyId
               """
        # 获取试剂数据
        med_data = BllMedicamentVariety().session.execute(SQL).fetchall()
        med_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(med_data)))
        data_list = []
        new_data_list = []
        # 便利数据合通过VarietyId相同合并字典
        for quarter in quarter_data:
            for year in year_data:
                if quarter['VarietyId'] == year['VarietyId']:
                    new_data = dict(quarter, **year)
                    data_list.append(new_data)
        for data_dict in data_list:
            for med in med_data:
                if data_dict['VarietyId'] == med['VarietyId']:
                    new_data = dict(data_dict, **med)
                    new_data_list.append(new_data)
        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 总共多少列data_list的长度
        data_list = ['试剂类别', '纯度', 'CAS码', '重点监管', '当前库存总量', '当前在库数量', '当前借出数量', '库存价值(元)',
                     '季度历史库存总量', '季度消耗总量', '季度消耗价值', '年度历史存库量', '年度消耗总量', '年度消耗价值']
        # 写入第一行第二行
        a.create_row1('库存试剂信息概览报表', len(data_list))
        a.create_row3(data_list)
        keys_list = ['Name', 'Purity', 'CASNumber', 'IsSupervise', 'TotalCount', 'NormalCount', 'UseCount',
                     'StockPrice', 'QuarterlyPutInCount', 'QuarterlyEmptyCount', 'QuarterlyEmptyPrice',
                     'YearPutInCount',
                     'YearEmptyCount', 'YearEmptyPrice']
        a.create_multiple_rows(4, new_data_list, keys_list)
        a.replace_space(len(keys_list))
        a.editor_isSupervise(string.ascii_uppercase[:14][keys_list.index('IsSupervise')])
        file_name = '库存试剂信息概览表{}'.format(Utils.UUID())
        a.save(file_name)
        response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
        response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        response['Content-Disposition'] = 'attachment;filename=' + urlquote("库存试剂信息概览表.xls")  # 注意filename 这个是下载后的名字
        response.set_cookie('fileDownload', True, 1)
        return response


# 导出数据明细报表
def exportDrugShelfLifeData(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        # client_id = request.GET.get('client_id', '')
        #
        # if client_id and client_id != 'undefined':
        #     SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament where RMS_Medicament.ClientId" \
        #           "=:client_id;"
        #     drug_obj_list = BllMedicament().execute(SQL, {'client_id': client_id}).fetchall()
        # else:
        #     searchWord = request.GET.get('searchWord', '')
        #     SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament "
        #     if searchWord and searchWord != 'undefined':
        #         SQL += " where RMS_Medicament.Name like :searchWord or RMS_Medicament.BarCode like :searchWord "
        #         drug_obj_list = BllMedicament().execute(SQL, {'searchWord': '%' + searchWord + '%'}).fetchall()
        #     else:
        #         drug_obj_list = BllMedicament().execute(SQL).fetchall()
        # drug_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))


        name = request.GET.get("searchValue", '')
        drug_list = BllMedicament().getAllDrugList(name, PageParam(1, 0))
        drug_obj_list = json.loads(Utils.resultAlchemyData(drug_list))

        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 定义总共多少列
        data_list = ['条形编号', '申购单编号', '采购单编号', '试剂类别', '所属项目', '试剂名称', '英文名称', 'CAS码',
                     '试剂余量（g）', '试剂规格', '纯度', '生产日期', '入库时间', '是否监管','状态','最后使用人','位置' ]
        # 写入第一行 第二行
        a.create_row1('试剂数据明细报表', len(data_list))

        # 写入第三行
        a.create_row3(data_list)
        # 写入有规律的多行数据
        keys_list = ['BarCode', 'Remark1', 'Remark2', 'Remark3', 'Remark4', 'Name', 'EnglishName',
                     'CASNumber', 'Remain', 'Speci', 'Purity',
                     'ProductionDate', 'PutInDate', 'IsSupervise','Status','ByUserName','Place']
        a.create_multiple_rows(4, drug_obj_list, keys_list)
        # 编辑空白替换为null
        a.replace_space(len(data_list))
        # 编辑试剂状态
        a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # 编辑试剂重点监管
        a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])

        file_name = '试剂数据明细报表{}'.format(Utils.getFileName())

        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("试剂数据明细报表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response



# 导出试剂流转记录报表函数
@require_http_methods(['GET'])
def exportDrugRecordData(request):
    if request.method == 'GET':
        client_id = request.GET.get('client_id', '')
        if client_id:
            SQL = "SELECT CreateDate,RecordType, RMS_Medicament.EnglishName, RMS_Medicament.Name, " \
                  "RMS_Medicament.BarCode, RMS_Medicament.ByUserName, RMS_Medicament.Purity, RMS_Medicament." \
                  "`Status`, RMS_Medicament.Place,`Status`, RMS_MedicamentRecord.CreateUserName, PutInUserName, CASNumber FROM `RMS_MedicamentRecord` INNER JOIN " \
                  " RMS_Medicament ON RMS_MedicamentRecord.MedicamentId = RMS_Medicament.MedicamentId WHERE " \
                  "RMS_Medicament.ClientId = :client_id;"
            report_record_list = BllMedicamentRecord().execute(SQL, {'client_id': client_id}).fetchall()
        else:
            SQL = "SELECT CreateDate,RecordType, RMS_Medicament.EnglishName, RMS_Medicament.Name, " \
                  "RMS_Medicament.BarCode, RMS_Medicament.ByUserName, RMS_MedicamentRecord.CreateUserName, RMS_Medicament.Purity, RMS_Medicament." \
                  "`Status`, RMS_Medicament.Place,`Status`, PutInUserName, CASNumber FROM `RMS_MedicamentRecord` INNER JOIN " \
                  " RMS_Medicament ON RMS_MedicamentRecord.MedicamentId = RMS_Medicament.MedicamentId;"
            report_record_list = BllMedicamentRecord().execute(SQL).fetchall()
        report_record_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(report_record_list)))

        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        data_list = ['条形编号', 'CAS码', '中文名称', '英文名称', '纯度', '操作人员', '操作类型', '目前状态',
                     '所属柜号', '记录日期', ]
        a.create_row1('试剂流转记录报表', len(data_list))
        a.create_row3(data_list)
        keys_list = ['BarCode', 'CASNumber', 'Name', 'EnglishName', 'Purity', 'CreateUserName', 'RecordType',
                     'Status', 'Place', 'CreateDate', ]
        a.create_multiple_rows(4, report_record_list, keys_list)
        a.editor_time(keys_list, 'CreateDate')
        a.replace_space(len(data_list))
        # 编辑试剂状态 string.ascii_uppercase[keys_list.index('Status')] 获取状态的列数
        a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # 编辑试剂类型
        a.editor_RecordType(string.ascii_uppercase[keys_list.index('RecordType')])
        file_name = '试剂流转记录报表{}'.format(Utils.UUID())
        a.save(file_name)
        response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
        response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        response['Content-Disposition'] = 'attachment;filename=' + urlquote("试剂流转记录报表.xls")  # 注意filename 这个是下载后的名字
        response.set_cookie('fileDownload', True, 1)
        return response


# 导出系统预警报表函数
@require_http_methods(['GET'])
def exportWarningData(request):
    if request.method == 'GET':
        SQL = """
            SELECT ObjectType, ObjectName, WarningContent, WarningDate, IsSolve, SolveDate, 
            SolveUserName, SolveContent FROM RMS_Warning order by WarningDate desc, IsSolve desc;
            """
        warning_record_list = BllWarning().execute(SQL).fetchall()
        warning_record_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(warning_record_list)))

        # 查询client温度上下线 湿度上下限
        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        data_list = ['预警类型', '预警对象', '预警内容', '预警时间', '状态', '处理时间', '处理人员', '处理方式', ]
        a.create_row1('系统预警数据记录报表', len(data_list))
        keys_list = ['ObjectType', 'ObjectName', 'WarningContent', 'WarningDate', 'IsSolve', 'SolveDate',
                     'SolveUserName', 'SolveContent', ]
        a.create_row3(data_list)
        a.create_multiple_rows(4, warning_record_list, keys_list)
        a.replace_space(len(data_list))
        # 替换解决类型
        a.max_lines = a.ws.max_row
        # 从第四行开始有规律
        for row_ in range(4, a.max_lines + 1):
            col_ = string.ascii_uppercase[keys_list.index('ObjectType')]
            b = a.ws[col_ + str(row_)].value
            if b == '1':
                a.ws[col_ + str(row_)].value = '试剂保质期预警'
            elif b == '2':
                a.ws[col_ + str(row_)].value = '试剂过期报警'
            elif b == '3':
                a.ws[col_ + str(row_)].value = '试剂余量预警'
            elif b == '4':
                a.ws[col_ + str(row_)].value = '药柜温湿度预警'
            elif b == '5':
                a.ws[col_ + str(row_)].value = '药柜滤芯保质期预警'
            elif b == '6':
                a.ws[col_ + str(row_)].value = '试剂出库超期预警'

        # 替换解决状态
        for row_ in range(4, a.max_lines + 1):
            col_ = string.ascii_uppercase[keys_list.index('IsSolve')]
            b = a.ws[col_ + str(row_)].value

            if b == 1:
                a.ws[col_ + str(row_)].value = '已解决'
            else:
                a.ws[col_ + str(row_)].value = '未解决'

        # 替换sqlAlchemy时间格式 预警时间
        a.editor_time(keys_list, 'WarningDate')

        # 处理sqlAlchemy时间格式 解决时间
        a.editor_time(keys_list, 'SolveDate')
        # 随机生成一个文件名
        file_name = '系统预警数据记录报表{}'.format(Utils.UUID())
        a.save(file_name)
        response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
        response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        response['Content-Disposition'] = 'attachment;filename=' + urlquote("系统预警数据记录报表.xlsx")  # 注意filename 这个是下载后的名字
        response.set_cookie('fileDownload', True, 1)
        return response


@require_http_methods(['GET'])
def exportUserData(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        data_user_list = BllUser().findList().all()
        data_user_list = json.loads(Utils.resultAlchemyData(data_user_list))

        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        data_list = ['工号', '角色', '姓名', '性别', 'QQ', '手机', '邮箱',
                     '条码', '状态', '最后一次登录时间', ]
        a.create_row1('用户角色数据统计表', len(data_list))
        a.create_row3(data_list)
        keys_list = ['UserCode', 'RoleName', 'RealName', 'Sex', 'QQ', 'Mobile', 'Email',
                     'BarCode', 'IsEnabled', 'LastVisitDate', ]
        a.create_multiple_rows(4, data_user_list, keys_list)
        a.replace_space(len(data_list))
        a.editor_time(keys_list, 'LastVisitDate')
        # 判断用户角色
        for row_ in range(4, a.max_lines + 1):
            col_ = string.ascii_uppercase[keys_list.index('UserCode')]
            b = a.ws[col_ + str(row_)].value
            if b == 'admin':
                for col_value in range(1, len(keys_list) + 1):
                    a.ws.cell(row=row_, column=col_value).fill = PatternFill(fill_type='solid', fgColor='FF0000')
            elif b == 'yanyi':
                for col_value in range(1, len(keys_list) + 1):
                    a.ws.cell(row=row_, column=col_value).fill = PatternFill(fill_type='solid', fgColor='FFFF00')

        # 优化用户性别
        for row_ in range(4, a.max_lines + 1):
            col_ = string.ascii_uppercase[keys_list.index('Sex')]
            b = a.ws[col_ + str(row_)].value
            if b == 0:
                a.ws[col_ + str(row_)].value = '女'
            else:
                a.ws[col_ + str(row_)].value = '男'
        a.editor_user_status('I')
        file_name = '用户角色数据统计表{}'.format(Utils.UUID())
        a.save(file_name)
        # 调用下载文件函数
        response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
        response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        # django自带一个urlquote函数用于url编码 解决中文识别问题
        response['Content-Disposition'] = 'attachment;filename=' + urlquote("用户角色数据统计表.xls")  # 注意filename 这个是下载后的名字
        response.set_cookie('fileDownload', True, 1)
        return response


# 导出所有报表数据
@require_http_methods(['GET'])
def exportAllReportData(request):
    if request.method == 'GET':
        SQL = """
        SELECT CreateDate,RecordType,ClientName,RMS_MedicamentRecord.ClientId, CreateUserName, RMS_Medicament.EnglishName, RMS_Medicament.Name, 
              RMS_Medicament.BarCode, RMS_Medicament.ByUserName, RMS_Medicament.Purity, RMS_Medicament.
              `Status`, RMS_Medicament.Place,`Status`, PutInUserName, CASNumber FROM `RMS_MedicamentRecord` INNER JOIN 
               RMS_Medicament ON RMS_MedicamentRecord.MedicamentId = RMS_Medicament.MedicamentId LEFT JOIN rms_client c on c.ClientId = RMS_MedicamentRecord.ClientId;
        """
        report_record_list = BllMedicamentRecord().execute(SQL).fetchall()
        report_record_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(report_record_list)))
        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='试剂流转记录报表')
        data_list = ['条形编号', 'CAS码', '中文名称', '英文名称', '纯度', '操作人员', '操作类型', '目前状态',
                     '所属柜号', '记录日期', ]
        a.create_row1('试剂流转记录报表', len(data_list))
        a.create_row3(data_list)
        keys_list = ['BarCode', 'CASNumber', 'Name', 'EnglishName', 'Purity', 'CreateUserName', 'RecordType',
                     'Status', 'ClientName', 'CreateDate', ]
        a.create_multiple_rows(4, report_record_list, keys_list)
        a.replace_space(len(data_list))
        # 编辑试剂状态 string.ascii_uppercase[keys_list.index('Status')] 获取状态的列数
        a.editor_time(keys_list, 'CreateDate')
        a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # 编辑试剂类型
        a.editor_RecordType(string.ascii_uppercase[keys_list.index('RecordType')])

        # 第二个sheet数据 -------------------------------------

        SQL = """
                        SELECT  b.VarietyId as VarietyId, COUNT(CASE when IsEmpty = 1 then 1 end) as QuarterlyEmptyCount, 
                              sum(CASE when IsEmpty = 1 then a.price else 0 end) as QuarterlyEmptyPrice, COUNT(CASE when RecordType = 1 then 1 end) as 
                              QuarterlyPutInCount from RMS_MedicamentVariety  as b LEFT JOIN RMS_MedicamentRecord as a on
                               b.VarietyId = a.VarietyId and QUARTER((a.CreateDate)) = QUARTER(now()) and Date_format
                              (a.CreateDate, '%Y') = (DATE_FORMAT(now(), '%Y')) GROUP by b.VarietyId
                        """
        # 获取季度数据
        quarter_data = BllMedicamentVariety().execute(SQL).fetchall()
        quarter_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(quarter_data)))
        SQL = """SELECT  b.VarietyId as VarietyId, COUNT(CASE when IsEmpty = 1 then a.CreateDate end) 
                              as YearEmptyCount, sum(CASE when IsEmpty = 1 then a.price else 0 end) as YearEmptyPrice,
                              COUNT(CASE when RecordType = 1 then 1 end) as YearPutInCount from RMS_MedicamentVariety  as b LEFT JOIN 
                              RMS_MedicamentRecord as a on b.VarietyId = a.VarietyId and year((a.CreateDate)) = 
                              year(now()) GROUP by b.VarietyId"""

        # 获取年度数据
        year_data = BllMedicamentVariety().session.execute(SQL).fetchall()
        year_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(year_data)))
        SQL = """
                   select  a.VarietyId as VarietyId, a.Name,a.Purity,a.CASNumber,a.IsSupervise, 
                   sum(case when b.`Status` = 1 then 1 else 0 end) as NormalCount,  
                   sum(case when b.`Status` = 1 or b.`Status` = 2 then 1 else 0 end) as TotalCount,
                   sum(case when b.`Status` = 2 then 1 else 0 end) as UseCount, 
                   sum(case when b.`Status` = 1 or b.`Status` = 2 then b.Price else 0 end)  as StockPrice 
                   from RMS_MedicamentVariety as a LEFT JOIN RMS_Medicament
                   as b on b.VarietyId = a.VarietyId GROUP BY a.VarietyId
               """
        # 获取试剂数据
        med_data = BllMedicamentVariety().session.execute(SQL).fetchall()
        med_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(med_data)))
        data_list = []
        new_data_list = []
        # 便利数据合通过VarietyId相同合并字典
        for quarter in quarter_data:
            for year in year_data:
                if quarter['VarietyId'] == year['VarietyId']:
                    new_data = dict(quarter, **year)
                    data_list.append(new_data)
        for data_dict in data_list:
            for med in med_data:
                if data_dict['VarietyId'] == med['VarietyId']:
                    new_data = dict(data_dict, **med)
                    new_data_list.append(new_data)

        # 创建第二个sheet
        a.set_style(title='库存试剂信息概览报表')
        # 总共多少列data_list的长度
        data_list = ['试剂类别', '纯度', 'CAS码', '重点监管', '当前库存总量', '当前在库数量', '当前借出数量', '库存价值(元)',
                     '季度历史库存总量', '季度消耗总量', '季度消耗价值', '年度历史存库量', '年度消耗总量', '年度消耗价值']
        # 写入第一行第二行
        a.create_row1('库存试剂信息概览报表', len(data_list))
        a.create_row3(data_list)
        keys_list = ['Name', 'Purity', 'CASNumber', 'IsSupervise', 'TotalCount', 'NormalCount', 'UseCount',
                     'StockPrice', 'QuarterlyPutInCount', 'QuarterlyEmptyCount', 'QuarterlyEmptyPrice',
                     'YearPutInCount',
                     'YearEmptyCount', 'YearEmptyPrice']
        a.create_multiple_rows(4, new_data_list, keys_list)
        a.replace_space(len(keys_list))
        a.editor_isSupervise(string.ascii_uppercase[:14][keys_list.index('IsSupervise')])

        # 第三个sheet表的数据  --------------------------

        SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament ORDER BY PutInDate desc;"
        drug_obj_list = BllMedicament().execute(SQL).fetchall()
        drug_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))
        # 创建第三个sheet表
        a.set_style(title='试剂数据明细报表')
        # 定义总共多少列
        data_list = ['条形编号', '中文名称', '英文名称', 'CAS码', '纯度', '价格(元/单位)', '目前状态', '生产日期',
                     '过期日期', '保质期(天)', '剩余有效天数(天)', '重点监管', '生产商家', '经销商', ]
        # 写入第一行 第二行
        a.create_row1('试剂数据明细报表', len(data_list))

        # 写入第三行
        a.create_row3(data_list)
        # 写入有规律的多行数据
        keys_list = ['BarCode', 'Name', 'EnglishName', 'CASNumber', 'Purity', 'Price', 'Status',
                     'ProductionDate', 'ExpirationDate', 'ShelfLife', 'SurplusDays',
                     'IsSupervise', 'Manufacturer', 'Distributor']
        a.create_multiple_rows(4, drug_obj_list, keys_list)
        # 编辑空白替换为null
        a.replace_space(len(data_list))
        # 编辑试剂状态
        a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # 编辑试剂重点监管
        a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])

        # 第四张表的数据 ----------------------------
        SQL = """
                        SELECT ObjectType, ObjectName, WarningContent, WarningDate, IsSolve, SolveDate, 
                        SolveUserName, SolveContent FROM RMS_Warning order by WarningDate desc, IsSolve desc;
                        """
        warning_record_list = BllWarning().execute(SQL).fetchall()
        warning_record_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(warning_record_list)))
        # 查询client温度上下线 湿度上下限
        # 创建第四张表
        a.set_style(title='系统预警数据记录报表')
        data_list = ['预警类型', '预警对象', '预警内容', '预警时间', '状态', '处理时间', '处理人员', '处理方式', ]
        a.create_row1('系统预警数据记录报表', len(data_list))
        keys_list = ['ObjectType', 'ObjectName', 'WarningContent', 'WarningDate', 'IsSolve', 'SolveDate',
                     'SolveUserName', 'SolveContent', ]
        a.create_row3(data_list)
        a.create_multiple_rows(4, warning_record_list, keys_list)
        a.replace_space(len(data_list))
        # 替换解决类型
        a.max_lines = a.ws.max_row
        for row_ in range(1, a.max_lines + 1):
            col_ = string.ascii_uppercase[keys_list.index('ObjectType')]
            b = a.ws[col_ + str(row_)].value
            if b == '1':
                a.ws[col_ + str(row_)].value = '试剂保质期预警'
            elif b == '2':
                a.ws[col_ + str(row_)].value = '试剂过期报警'
            elif b == '3':
                a.ws[col_ + str(row_)].value = '试剂余量预警'
            elif b == '4':
                a.ws[col_ + str(row_)].value = '药柜温湿度预警'
            elif b == '5':
                a.ws[col_ + str(row_)].value = '药柜滤芯保质期预警'
            elif b == '6':
                a.ws[col_ + str(row_)].value = '试剂出库超期预警'

        # 替换解决状态
        for row_ in range(1, a.max_lines + 1):
            col_ = string.ascii_uppercase[keys_list.index('IsSolve')]
            b = a.ws[col_ + str(row_)].value
            if b == 1:
                a.ws[col_ + str(row_)].value = '已解决'
            else:
                a.ws[col_ + str(row_)].value = '未解决'

        # 替换sqlAlchemy时间格式 预警时间
        a.editor_time(keys_list, 'WarningDate')
        # 处理sqlAlchemy时间格式 解决时间
        a.editor_time(keys_list, 'SolveDate')

        # 获取第五张表的数据 ---------------------
        data_user_list = BllUser().findList().all()
        data_user_list = json.loads(Utils.resultAlchemyData(data_user_list))

        # 创建第五张表
        a.set_style(title='用户角色数据统计报表')
        data_list = ['工号', '角色', '姓名', '性别', 'QQ', '手机', '邮箱',
                     '条码', '状态', '最后一次登录时间', ]
        a.create_row1('用户角色数据统计表', len(data_list))
        a.create_row3(data_list)
        keys_list = ['UserCode', 'RoleName', 'RealName', 'Sex', 'QQ', 'Mobile', 'Email',
                     'BarCode', 'IsEnabled', 'LastVisitDate', ]
        a.create_multiple_rows(4, data_user_list, keys_list)
        a.replace_space(len(data_list))
        a.editor_time(keys_list, 'LastVisitDate')
        a.editor_user_status('I')

        # 优化用户性别
        for row_ in range(4, a.max_lines + 1):
            col_ = string.ascii_uppercase[keys_list.index('Sex')]
            b = a.ws[col_ + str(row_)].value
            if b == 0:
                a.ws[col_ + str(row_)].value = '女'
            else:
                a.ws[col_ + str(row_)].value = '男'

        # 判断用户角色
        for row_ in range(1, a.max_lines + 1):
            col_ = string.ascii_uppercase[keys_list.index('UserCode')]
            b = a.ws[col_ + str(row_)].value
            if b == 'admin':
                for col_value in range(1, len(keys_list) + 1):
                    a.ws.cell(row=row_, column=col_value).fill = PatternFill(fill_type='solid', fgColor='FF0000')
            elif b == 'yanyi':
                for col_value in range(1, len(keys_list) + 1):
                    a.ws.cell(row=row_, column=col_value).fill = PatternFill(fill_type='solid', fgColor='FFFF00')

        excel_name = '所有报表数据{}'.format(Utils.UUID())
        a.save(excel_name)
        response = StreamingHttpResponse(ReportData.download_excel(excel_name + '.xlsx'))
        response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        # django自带一个urlquote函数用于url编码 解决中文识别问题
        response['Content-Disposition'] = 'attachment;filename=' + urlquote("报表数据综合.xlsx")
        response.set_cookie('fileDownload', True, 1)
        return response


# 库存信息总览
@require_http_methods(['GET'])
def getOverviewInfo(request):
    return render(request, 'dataReport/newDrugOverviewInfo.html', locals())


# 入库信息查询
@require_http_methods(['GET'])
def getPutInInfo(request):
    return render(request, 'dataReport/newPutInInfo.html', locals())


# 使用频率统计
@require_http_methods(['GET'])
def getUseFrequencyInfo(request):
    return render(request, 'dataReport/newDrugUseFrequencyInfo.html', locals())


# 消耗统计
@require_http_methods(['GET'])
def getDrugConsumeInfo(request):
    endDate = (date.today() + relativedelta.relativedelta(days=1)).strftime('%Y-%m-%d')
    startDate = (date.today() + relativedelta.relativedelta(years=-1, days=1)).strftime('%Y-%m-%d')
    return render(request, 'dataReport/newDrugConsumeInfo.html', locals())


# 保质期统计
@require_http_methods(['GET'])
def getShelflifeInfo(request):
    return render(request, 'dataReport/newShelflifeInfo.html', locals())


# 保质期预警统计
@require_http_methods(['GET'])
def getShelflifeWarning(request):
    return render(request, 'dataReport/newShelflifeWarningInfo.html', locals())


# 库存呆滞料统计
@require_http_methods(['GET'])
def getStagnantInfo(request):
    return render(request, 'dataReport/newDrugStagnantInfo.html', locals())


# 试剂历史使用信息统计
@require_http_methods(['GET'])
def getDrugUseRecordInfo(request):
    return render(request, 'dataReport/newDrugUseRecordInfo.html', locals())


# 人员用量统计
@require_http_methods(['GET'])
def getUserConsumeInfo(request):
    return render(request, 'dataReport/newtUserConsumeInfo.html', locals())


# 试剂种类消耗统计
@require_http_methods(['GET'])
def getDrugUseCategotyConsumeInfo(request):
    return render(request, 'dataReport/newDrugUseCategotyConsumeInfo.html', locals())


#试剂详细信息统计
@require_http_methods(['GET'])
def getDrugDetailInfo(request):
    return render(request, 'dataReport/newDrugDetailInfo.html', locals())


#返回库存总览Json数据
# 返回库存总览Json数据
@require_http_methods(['GET'])
def getOverviewInfoJson(request):
    if request.method == 'GET':
        name = request.GET.get("name", '')
        SQL_str = ''
        if name:
            SQL_str = 'WHERE b.Name = "{0}"'.format(name.strip())
        try:
            SQL = """
                    SELECT b.Name, b.Speci,SUM(CASE when a.`Status`=1  then 1 else 0 end) as NormalCount,a.SpeciUnit, a.Price,SUM(CASE when a.`Status`=1  then a.Remain else 0 end) as quality,b.CASNumber,
                    SUM(CASE when a.`Status`=1  then a.Price else 0 end) as "TotalPrice" FROM RMS_Medicament as 
                    a LEFT JOIN RMS_MedicamentVariety as b on b.VarietyId = a.VarietyId {0} GROUP by b.VarietyId order by a.PutInDate asc; """.format(SQL_str)

            backup_sql = """
                SELECT a.VarietyId,b.Name, b.Speci, COUNT(a.MedicamentId) as NormalCount,a.SpeciUnit, a.Price, b.CASNumber,
                SUM(CASE when a.`Status`=1 then a.Price else 0 end) as "TotalPrice" FROM RMS_Medicament as 
                a LEFT JOIN RMS_MedicamentVariety as b on b.VarietyId = a.VarietyId {0} GROUP by a.VarietyId order by a.PutInDate asc;
            """.format(SQL_str)
            drug_obj_list = BllWarning().execute(SQL).fetchall()
            print(drug_obj_list)
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})
        except:
            logger.debug('数据库操作失败')
            BllMedicament().session.rollback()
            drug_obj_list = []
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})


# 返回入库Json数据
@require_http_methods(['GET'])
def getPutInInfoJson(request):
    if request.method == 'GET':
        try:
            name = request.GET.get('searchValue', '')
            manu = request.GET.get('manufacturer', '')
            put_in_date = request.GET.get('putInDateStart', '')
            put_in_end = request.GET.get('putInDateEnd', '')

            search_dict = {
                "Name=": request.GET.get('searchValue', ''),
                "Manufacturer=": request.GET.get('manufacturer', ''),
                "DATE_FORMAT(PutInDate,'%Y-%m-%d %H:%M:%S') >=": request.GET.get('putInDateStart', ''),
                "DATE_FORMAT(PutInDate,'%Y-%m-%d %H:%M:%S') <=": request.GET.get('putInDateEnd', '')
            }
            param_str = ''
            for key, value in search_dict.items():
                if search_dict[key] != '':
                    param_str = param_str + "{0}'{1}' and ".format(key, value)
            if param_str != '':
                param_str = 'WHERE {0}'.format(param_str.strip(' and '))
                SQL = """
                SELECT Name, Speci, Remain,SpeciUnit,Manufacturer,PutInDate,PutInUserId,PutInUserName,ProductionDate,ExpirationDate,ShelfLife FROM RMS_Medicament {0} order by PutInDate asc;
                """.format(param_str)
            else:
                SQL = """
                SELECT Name, Speci, Remain,SpeciUnit,Manufacturer,PutInDate,PutInUserId,PutInUserName,ProductionDate,ExpirationDate,ShelfLife FROM RMS_Medicament order by PutInDate asc;
                """
            drug_obj_list = BllMedicament().execute(SQL).fetchall()
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})
        except:
            logger.debug('数据库操作失败')
            BllMedicament().session.rollback()
            drug_obj_list = []
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})


# 返回使用频率json数据#mmm
@require_http_methods(['GET'])
def getUseFrequencyInfoJson(request):
    if request.method == 'GET':
        try:
            # client_id = request.GET.get('clientId', '')
            name = request.GET.get('searchValue', '')
            record_date_start = request.GET.get('recordDateStart', '')
            record_date_end = request.GET.get('recordDateEnd', '')

            search_dict = {
                "Name=": request.GET.get('searchValue', ''),
                "DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S') >=": request.GET.get('recordDateStart', ''),
                "DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S') <=": request.GET.get('recordDateEnd', '')
            }
            param_str = ''
            for key, value in search_dict.items():
                if search_dict[key] != '':
                    param_str = param_str + "{0}'{1}' and ".format(key, value)
            if param_str != '':
                param_str = 'WHERE {0}'.format(param_str.strip(' and '))
                SQL = """
                SELECT b.Name, SUM(CASE WHEN a.RecordType=1 then 1 else 0 end) as TotalCount, b.Speci,b.SpeciUnit,b.Purity,
                min(DATE_FORMAT(a.CreateDate, '%Y-%m-%d %H:%i:%S')) as minTime,
                max(DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S'))as maxTime, 
                SUM(CASE WHEN a.RecordType=2 then 1 else 0 end) as usedTimes,
                SUM(CASE WHEN a.RecordType=3 then 1 else 0 end) as returnTimes
                FROM rms_medicamentrecord as a RIGHT join rms_medicamentvariety as b on a.VarietyId=b.VarietyId
                {0}       
                GROUP BY b.VarietyId;
                """.format(param_str)
            else:
                SQL = """
                SELECT b.Name, SUM(CASE WHEN a.RecordType=1 then 1 else 0 end) as TotalCount, b.Speci,b.SpeciUnit,b.Purity,
                min(DATE_FORMAT(a.CreateDate, '%Y-%m-%d %H:%i:%S')) as minTime,
                max(DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S'))as maxTime, 
                SUM(CASE WHEN a.RecordType=2 then 1 else 0 end) as usedTimes,
                SUM(CASE WHEN a.RecordType=3 then 1 else 0 end) as returnTimes
                FROM rms_medicamentrecord as a RIGHT join rms_medicamentvariety as b on a.VarietyId=b.VarietyId      
                GROUP BY b.VarietyId;
                """
            drug_obj_list = BllMedicament().execute(SQL).fetchall()
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})
        except:
            logger.debug('数据库操作失败')
            BllMedicament().session.rollback()
            drug_obj_list = []
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})


# # 返回消耗统计json数据
# @require_http_methods(['GET'])
# def getDrugConsumeInfoJson(request):
#     if request.method == 'GET':
#         startDate = request.GET.get('startDate','')
#         endDate = request.GET.get('endDate','')
#         print('shishishishsi',startDate,endDate)
#         if startDate:
#             if endDate:
#                 str1 = " WHERE a.CreateDate BETWEEN :startDate AND :endDate GROUP by b.VarietyId"
#             else:
#                 str1 = " WHERE a.CreateDate>:startDate GROUP by b.VarietyId"
#         else:
#             if endDate:
#                 str1 = " WHERE a.CreateDate<:endDate GROUP by b.VarietyId"
#             else:
#                 str1 = ' GROUP by b.VarietyId'
#         SQL_a = """SELECT  b.VarietyId as VarietyId, COUNT(CASE when IsEmpty = 1 then 1 end) as QuarterlyEmptyCount,
#                               sum(CASE when IsEmpty = 1 then a.price else 0 end) as QuarterlyEmptyPrice, COUNT(CASE when RecordType = 1 then 1 end) as
#                               QuarterlyPutInCount from RMS_MedicamentVariety  as b LEFT JOIN RMS_MedicamentRecord as a on
#                                b.VarietyId = a.VarietyId and QUARTER((a.CreateDate)) = QUARTER(now()) and Date_format
#                               (a.CreateDate, '%Y') = (DATE_FORMAT(now(), '%Y'))"""
#         SQL = SQL_a + str1
#         # print('sql yuju shi ',SQL)
#         # 获取季度数据
#         quarter_data = BllMedicamentVariety().execute(SQL,{'startDate': startDate, 'endDate': endDate}).fetchall()
#         quarter_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(quarter_data)))
#         SQL = """SELECT  b.VarietyId as VarietyId, COUNT(CASE when IsEmpty = 1 then a.CreateDate end)
#                               as YearEmptyCount, sum(CASE when IsEmpty = 1 then a.price else 0 end) as YearEmptyPrice,
#                               COUNT(CASE when RecordType = 1 then 1 end) as YearPutInCount from RMS_MedicamentVariety  as b LEFT JOIN
#                               RMS_MedicamentRecord as a on b.VarietyId = a.VarietyId and year((a.CreateDate)) =
#                               year(now()) GROUP by b.VarietyId"""
#
#         # 获取年度数据
#         year_data = BllMedicamentVariety().session.execute(SQL).fetchall()
#         year_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(year_data)))
#         SQL = """
#             select  a.VarietyId as VarietyId, a.Name,a.Purity,a.CASNumber,a.IsSupervise, b.Price,
#             sum(case when b.`Status` = 1 then 1 else 0 end) as NormalCount,
#             sum(case when b.`Status` = 1 or b.`Status` = 2 then 1 else 0 end) as TotalCount,
#             sum(case when b.`Status` = 2 then 1 else 0 end) as UseCount,
#             sum(case when b.`Status` = 1 or b.`Status` = 2 then b.Price else 0 end)  as StockPrice
#             from RMS_MedicamentVariety as a LEFT JOIN RMS_Medicament
#             as b on b.VarietyId = a.VarietyId GROUP BY a.VarietyId
#         """
#         # 获取试剂数据
#         med_data = BllMedicamentVariety().execute(SQL).fetchall()
#         med_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(med_data)))
#         data_list = []
#         new_data_list = []
#         # 便利数据合通过VarietyId相同合并字典
#         for quarter in quarter_data:
#             for year in year_data:
#                 if quarter['VarietyId'] == year['VarietyId']:
#                     new_data = dict(quarter, **year)
#                     data_list.append(new_data)
#         for data_dict in data_list:
#             for med in med_data:
#                 if data_dict['VarietyId'] == med['VarietyId']:
#                     new_data = dict(data_dict, **med)
#                     new_data_list.append(new_data)
#         return JsonResponse({'data': json.loads(Utils.resultAlchemyData(new_data_list))})

# 返回消耗统计json数据
@require_http_methods(['GET'])
def getDrugConsumeInfoJson(request):
    if request.method == 'GET':
        search_dict = {
            'Name': request.GET.get('searchValue', ''),
            "DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S') >=": request.GET.get('startDate', ''),
            "DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S') <=": request.GET.get('endDate', '')
        }
        param_str = ''
        for key, value in search_dict.items():
            if search_dict[key] != '':
                param_str = param_str + "{0}'{1}' and ".format(key, value)
        if param_str != '':
            param_str = 'WHERE {0}'.format(param_str.strip(' and '))

        SQL_a = """SELECT  b.VarietyId as VarietyId, COUNT(CASE when IsEmpty = 1 then 1 end) as QuarterlyEmptyCount, 
                                     sum(CASE when IsEmpty = 1 then a.price else 0 end) as QuarterlyEmptyPrice,COUNT(CASE when RecordType = 1 then 1 end) as RecordType from RMS_MedicamentVariety  as b LEFT JOIN RMS_MedicamentRecord as a on
                                      b.VarietyId = a.VarietyId {0} GROUP by b.VarietyId""".format(param_str)
        print('第一ci记录',SQL_a)
        # 获取试剂消耗数据
        quarter_data = BllMedicamentVariety().execute(SQL_a).fetchall()
        quarter_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(quarter_data)))

        SQL = """
                   select  a.VarietyId as VarietyId, a.Name,a.Purity,a.CASNumber,a.IsSupervise, b.Price,
                   sum(case when b.`Status` = 1 then 1 else 0 end) as NormalCount,  
                   sum(case when b.`Status` = 1 or b.`Status` = 2 then 1 else 0 end) as TotalCount,
                   sum(case when b.`Status` = 2 then 1 else 0 end) as UseCount, 
                   sum(case when b.`Status` = 1 or b.`Status` = 2 then b.Price else 0 end)  as StockPrice 
                   from RMS_MedicamentVariety as a LEFT JOIN RMS_Medicament
                   as b on b.VarietyId = a.VarietyId GROUP BY a.VarietyId
               """
        # 获取试剂数据
        med_data = BllMedicamentVariety().execute(SQL).fetchall()
        med_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(med_data)))
        new_data_list = []
        # 遍历数据通过VarietyID相同合并字典
        for quarter in quarter_data:
            for med in med_data:
                if quarter['VarietyId'] == med['VarietyId']:
                    new_data = dict(quarter, **med)
                    new_data_list.append(new_data)

        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(new_data_list))})

# 返回保质期统计json数据
@require_http_methods(['GET'])
def getShelflifeInfoJson(request):
    if request.method == 'GET':
        searchValue = request.GET.get("searchValue", '')
        SQL_str = ''
        if searchValue:
            SQL_str = 'WHERE RMS_Medicament.Name = "{0}"'.format(searchValue.strip())
        try:
            SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament {0} ORDER BY SurplusDays ASC;".format(SQL_str)
            drug_obj_list = BllMedicament().execute(SQL).fetchall()
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})
        except:
            logger.debug('数据库操作失败')
            BllMedicament().session.rollback()


# 返回保质期预警统计json数据
@require_http_methods(['GET'])
def getShelflifeWarningJson(request):
    if request.method == 'GET':
        warningDays = request.GET.get('WarningDays', '')
        try:
            SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament  where " \
                  "DATEDIFF(ExpirationDate,now()) < :warningDays ORDER BY SurplusDays ASC;"
            drug_obj_list = BllMedicament().execute(SQL, {'warningDays': warningDays}).fetchall()
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})
        except:
            logger.debug('数据库操作失败')
            BllMedicament().session.rollback()


# 返回库存呆滞json数据
@require_http_methods(['GET'])
def getStagnantInfoJson(request):
    if request.method == 'GET':
        try:
            SQL = "SELECT * FROM ( SELECT RMS_Medicament.*, DATEDIFF(ProductionDate,now()) as StagnantDays,Count(CASE when rms_medicamentrecord.RecordType != 1 then 1 end) AS useCount from RMS_Medicament " \
                  " LEFT JOIN rms_medicamentrecord ON RMS_Medicament.MedicamentId=rms_medicamentrecord.MedicamentId  ) as T WHERE T.useCount=0  ORDER BY T.StagnantDays DESC LIMIT 20;"
            drug_obj_list = BllMedicament().execute(SQL).fetchall()
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))})
        except:
            logger.debug('数据库操作失败')
            BllMedicament().session.rollback()


# 返回试剂历史使用json数据
@require_http_methods(['GET'])
def getDrugUseRecordInfoJson(request):
    if request.method == 'GET':
        # 获取当前选择年份
        year = request.GET.get('year')
        SQL = """
        SELECT a.CreateDate, sum( CASE when a.RecordType = 1 then 1 else 0 end) as 'putInCountList', 
        sum( CASE when a.RecordType = 2 then 1 else 0 end) as 'useCountList', 
        sum( CASE when a.RecordType = 3 then 1 else 0 end) as 'returnCountList' from RMS_MedicamentRecord 
            as a WHERE DATE_FORMAT(a.CreateDate, '%Y') = :year GROUP by DATE_FORMAT(a.CreateDate, '%Y-%m')
        """
        # 当前月份
        now_month = datetime.datetime.now().strftime('%m')
        # 当前年份
        current_year = datetime.datetime.now().strftime('%Y')
        # 获取数据库入库, 借出, 归还数据
        HumitureRecord_obj_list = BllHumitureRecord().execute(SQL, {'year': year}).fetchall()
        # 把列表对象转化成列表字典类型
        HumitureRecord_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(HumitureRecord_obj_list)))
        # 入库
        putInCountList = []
        # 借出
        useCountList = []
        # 归还
        returnCountList = []
        # 月份列表
        month_list = []

        if year == current_year:
            now_month = int(now_month)
        else:
            now_month = 12

        for x in range(now_month):
            # 当月份小于10 格式化为0x月格式 x是从0开始所有应该是小于9
            if x < 9:
                x = '0' + str(x + 1)
            else:
                x += 1
            for HumitureRecord_obj in HumitureRecord_obj_list:
                # 判断当前遍历月份是否等于数据库存在的月份, 如果等于就给得到的值, 否则增加0
                if HumitureRecord_obj['CreateDate'][5:7] == str(x):
                    putInCountList.append(int(HumitureRecord_obj['putInCountList']))
                    useCountList.append(int(HumitureRecord_obj['useCountList']))
                    returnCountList.append(int(HumitureRecord_obj['returnCountList']))
                    # 有就跳出循环
                    break
            else:
                # 如果正常循环, 则代表数据库没有此月份, 就增加数值0
                putInCountList.append(0)
                useCountList.append(0)
                returnCountList.append(0)
            month_list.append(str(x) + '月')

        # 返回前段展示的data数据
        data = {"xAxisList": month_list, "putInCountList": putInCountList, "useCountList": useCountList,
                "returnCountList": returnCountList}

        return JsonResponse({'data': data})


# 返回人员用量统计json数据
@require_http_methods(['GET'])
def getUserConsumeInfoJson(request):
    if request.method == 'GET':
        startDate = request.GET.get('startDate', '')
        endDate = request.GET.get('endDate', '')
        print('mxh_开始结束时间是：',startDate,endDate)
        #mxh_数据库筛选条件
        user_consume_obj_json = UserConsumeInfoJsonSelect(startDate,endDate)
        return JsonResponse({'data': user_consume_obj_json})
#mxh_人员用量统计_数据库选择
def UserConsumeInfoJsonSelect(startDate,endDate):
    if startDate:
        if endDate:
            sql_where = ' and (RMS_MedicamentRecord.CreateDate BETWEEN :startDate AND :endDate) GROUP BY CreateUserId ORDER BY SUM(UseQuantity) DESC;'
        else:
            sql_where = ' and (RMS_MedicamentRecord.CreateDate>:startDate) GROUP BY CreateUserId ORDER BY SUM(UseQuantity) DESC;'
    else:
        if endDate:
            sql_where = ' and (RMS_MedicamentRecord.CreateDate<:endDate) GROUP BY CreateUserId ORDER BY SUM(UseQuantity) DESC;'
        else:
            sql_where = ' GROUP BY CreateUserId ORDER BY SUM(UseQuantity) DESC;'
    try:
        print('mxh_开始查询get')
        SQL_a = "SELECT CreateUserName as UsePeople,  COUNT(*) AS UseCount, SUM(UseQuantity) AS TotalUseQuantity ,SUM(UseQuantity)/(SELECT SUM(UseQuantity) FROM rms_medicamentrecord) AS UseQuantityPercent " \
                " FROM rms_medicamentrecord WHERE RecordType=3"
        SQL = SQL_a + sql_where
        user_consume_obj_list = BllMedicament().execute(SQL, {'startDate': startDate, 'endDate': endDate}).fetchall()
        print('测试数据：',user_consume_obj_list)
        user_consume_obj_json = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(user_consume_obj_list)))
        print('得到数据：',user_consume_obj_json)
        return user_consume_obj_json
    except:
        logger.debug('数据库操作失败')
        user_consume_obj_json = ''
        BllMedicament().session.rollback()
        return user_consume_obj_json


#mxh_下载人员消耗试剂信息统计报表
@require_http_methods(['GET'])
def downUserConsumeInfoJson(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        startDate = request.GET.get('startDate', '')
        endDate = request.GET.get('endDate', '')
        print('mxh_开始结束时间是：',startDate,endDate)
        #mxh_数据库筛选条件
        user_consume_obj_json = UserConsumeInfoJsonSelect(startDate,endDate)

        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 定义总共多少列
        data_list = ['用户名称','使用次数','总用量（g)','占用百分比']
        # 写入第一行 第二行
        a.create_row1('人员消耗试剂信息统计报表', len(data_list))

        # 写入第三行
        a.create_row3(data_list)
        # 写入有规律的多行数据
        keys_list = ['UsePeople', 'UseCount', 'TotalUseQuantity', 'UseQuantityPercent']
        a.create_multiple_rows(4, user_consume_obj_json, keys_list)
        # 编辑空白替换为null
        a.replace_space(len(data_list))
        # # 编辑试剂状态
        # a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # # 编辑试剂重点监管
        # a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])


        file_name = '人员消耗试剂信息统计报表{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("人员消耗试剂信息统计报表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response

# mxh_返回试剂种类消耗统计json数据
@require_http_methods(['GET'])
def getDrugUseCategotyConsumeInfoJson(request):
    if request.method == 'GET':
        startDate = request.GET.get('startDate', '')
        endDate = request.GET.get('endDate', '')
        categoty_consum_json = DrugUseCategotyConsumeInfoSelect(startDate,endDate)
        return JsonResponse({'data': categoty_consum_json})

#mxh_试剂种类消耗统计_数据库选择
def DrugUseCategotyConsumeInfoSelect(startDate,endDate):
    if startDate:
        if endDate:
            sql_where = ' and (m.CreateDate BETWEEN :startDate AND :endDate) GROUP BY m.VarietyId ORDER BY SUM(UseQuantity) DESC;'
        else:
            sql_where = ' and (m.CreateDate>:startDate) GROUP BY m.VarietyId ORDER BY SUM(UseQuantity) DESC;'
    else:
        if endDate:
            sql_where = ' and (m.CreateDate<:endDate) GROUP BY m.VarietyId ORDER BY SUM(UseQuantity) DESC;'
        else:
            sql_where = ' GROUP BY m.VarietyId ORDER BY SUM(UseQuantity) DESC;'
    try:
        SQL_a = "SELECT me.Name,me.EnglishName,me.Purity,me.Speci,me.SpeciUnit,me.CASNumber,sum(CASE when me1.ByUserName is NULL then 1 else 0 end) AS NormalCount,sum(CASE when m.RecordType = 1 then 1 else 0 end) AS PutInCount,sum(CASE when m.IsEmpty = 1 then 1 else 0 end) AS EmptyCount,  sum(CASE when m.RecordType = 2 then 1 else 0 end) AS UseCount, SUM(UseQuantity) AS TotalUseQuantity ,SUM(UseQuantity)/(SELECT SUM(UseQuantity) FROM rms_medicamentrecord) AS UseQuantityPercent " \
                " FROM rms_medicamentrecord m RIGHT JOIN rms_medicament me1 ON me1.MedicamentId=m.MedicamentId RIGHT JOIN rms_medicamentvariety me ON m.VarietyId=me.VarietyId  "
        SQL = SQL_a + sql_where
        categoty_consum_list = BllMedicament().execute(SQL, {'startDate': startDate, 'endDate': endDate}).fetchall()
        categoty_consum_json = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(categoty_consum_list)))
        return categoty_consum_json
    except:
        logger.debug('数据库操作失败')
        categoty_consum_json = ''
        BllMedicament().session.rollback()
        return categoty_consum_json

#mxh_下载试剂种类消耗统计报表
@require_http_methods(['GET'])
def downDrugUseCategotyConsumeInfoJson(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        startDate = request.GET.get('startDate', '')
        endDate = request.GET.get('endDate', '')
        categoty_consum_json = DrugUseCategotyConsumeInfoSelect(startDate,endDate)

        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 定义总共多少列
        data_list = ['试剂名称', '英文名称', 'CAS码', '纯度','规格','使用次数','总用量(g)','占用百分比(%)']
        # 写入第一行 第二行
        a.create_row1('试剂种类消耗信息统计报表', len(data_list))

        # 写入第三行
        a.create_row3(data_list)
        # 写入有规律的多行数据
        keys_list = ['Name', 'EnglishName', 'CASNumber', 'Purity','Speci','UseCount','Speci','UseQuantityPercent']
        a.create_multiple_rows(4, categoty_consum_json, keys_list)
        # 编辑空白替换为null
        a.replace_space(len(data_list))
        # # 编辑试剂状态
        # a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # # 编辑试剂重点监管
        # a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])


        file_name = '试剂种类消耗信息统计报表{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("试剂种类消耗信息统计报表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response

#返回试剂详细信息统计json数据
@require_http_methods(['GET'])
def getDrugDetailInfoJson(request):
    if request.method == 'GET':
        drug_list = BllMedicament().getAllDrugList(request.GET['searchValue'], PageParam(1, 0))
        return JsonResponse({'data': drug_list})


#下载库存总览表
# 下载库存总览表
@require_http_methods(['GET'])
def downOverviewInfo(request):
    # if request.method == 'GET':
    #     name = request.GET.get("name", '')
    #     if name:
    #         SQL = """
    #             SELECT b.Name, b.Speci,COUNT(a.MedicamentId) as NormalCount,a.Price, SUM(Remain) as quality, b.CASNumber,
    #             SUM(CASE when a.`Status`=1  then a.Price else 0 end) as "TotalPrice" FROM RMS_Medicament as
    #             a LEFT JOIN RMS_MedicamentVariety as b on b.VarietyId = a.VarietyId where b.Name='{}'
    #             and a.VarietyId IS NOT NULL and b.VarietyId IS NOT NULL
    #             GROUP by b.VarietyId order by a.PutInDate asc;
    #         """.format(name)
    #     else:
    #         SQL = """
    #                 SELECT b.Name, b.Speci, COUNT(a.MedicamentId) as NormalCount, a.Price, SUM(Remain) as quality, b.CASNumber,
    #                 SUM(CASE when a.`Status`=1  then a.Price else 0 end) as "TotalPrice" FROM RMS_Medicament as
    #                 a LEFT JOIN RMS_MedicamentVariety as b on b.VarietyId = a.VarietyId
    #                 WHERE a.VarietyId IS NOT NULL and b.VarietyId IS NOT NULL
    #                 GROUP by b.VarietyId order by a.PutInDate asc;
    #         """
    #     report_record_list = BllMedicamentRecord().execute(SQL).fetchall()
    #     report_record_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(report_record_list)))

    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        name = request.GET.get("name", '')
        SQL_str = ''
        if name:
            SQL_str = 'WHERE b.Name = "{0}"'.format(name.strip())
        try:
            print('sql_str is ',SQL_str)
            SQL = """
                    SELECT b.Name, b.Speci,SUM(CASE when a.`Status`=1  then 1 else 0 end) as NormalCount,a.SpeciUnit, a.Price, SUM(CASE when a.`Status`=1  then a.Remain else 0 end) as quality,b.CASNumber,
                    SUM(CASE when a.`Status`=1  then a.Price else 0 end) as "TotalPrice" FROM RMS_Medicament as 
                    a LEFT JOIN RMS_MedicamentVariety as b on b.VarietyId = a.VarietyId {0} GROUP by b.VarietyId order by a.PutInDate asc; """.format(
                SQL_str)
            print('SQL is ',SQL)
            drug_obj_list = BllWarning().execute(SQL).fetchall()
            report_record_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))
        except:
            logger.debug('数据库操作失败')
            BllMedicament().session.rollback()
            drug_obj_list = []
            report_record_list = ''

        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        data_list = ['试剂名称', 'CAS码', '规格', '在库剩余数量(瓶)', '在库剩余总质量(g)', '在库总价（元）']
        a.create_row1('库存试剂总览统计', len(data_list))
        a.create_row3(data_list)
        keys_list = ['Name', 'CASNumber', 'Speci', 'NormalCount', 'quality', 'TotalPrice']
        a.create_multiple_rows(4, report_record_list, keys_list)
        # a.editor_time(keys_list, 'CreateDate')
        a.replace_space(len(data_list))
        # # 编辑试剂状态 string.ascii_uppercase[keys_list.index('Status')] 获取状态的列数
        # a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # # 编辑试剂类型
        # a.editor_RecordType(string.ascii_uppercase[keys_list.index('RecordType')])
        file_name = '库存试剂总览表{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("库存试剂总览表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response


# 下载入库信息表
@require_http_methods(['GET'])
def downPutInInfo(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        search_dict = {
            "Name=": request.GET.get('searchValue', ''),
            "Manufacturer=": request.GET.get('manufacturer', ''),
            "DATE_FORMAT(PutInDate,'%Y-%m-%d %H:%M:%S') >=": request.GET.get('putInDateStart', ''),
            "DATE_FORMAT(PutInDate,'%Y-%m-%d %H:%M:%S') <=": request.GET.get('putInDateEnd', '')
        }
        param_str = ''
        for key, value in search_dict.items():
            if search_dict[key] != '':
                param_str = param_str + "{0}'{1}' and ".format(key, value)
        if param_str != '':
            param_str = 'WHERE {0}'.format(param_str.strip(' and '))
            SQL = """
                            SELECT Name, Speci, Remain,SpeciUnit,Manufacturer,PutInDate,PutInUserId,PutInUserName,ProductionDate,ExpirationDate,ShelfLife FROM RMS_Medicament {0} order by PutInDate asc;
                            """.format(param_str)
        else:
            SQL = """
                            SELECT Name, Speci, Remain,SpeciUnit,Manufacturer,PutInDate,PutInUserId,PutInUserName,ProductionDate,ExpirationDate,ShelfLife FROM RMS_Medicament order by PutInDate asc;
                            """

        drug_obj_list = BllMedicament().execute(SQL).fetchall()
        drug_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))
        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 定义总共多少列
        data_list = ['名称', '规格', '生产厂商', '余量(g)', "生产日期", "过期日期", "保质期","入库人",'入库时间']
        # 写入第一行 第二行
        a.create_row1('入库信息报表', len(data_list))

        # 写入第三行
        a.create_row3(data_list)
        # 写入有规律的多行数据
        keys_list = ['Name', 'Speci', 'Manufacturer', 'Remain', 'ProductionDate', 'ExpirationDate', 'ShelfLife', 'PutInUserName','PutInDate']
        a.create_multiple_rows(4, drug_obj_list, keys_list)
        # 编辑空白替换为null
        a.replace_space(len(data_list))
        # 编辑试剂状态
        # a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # 编辑试剂重点监管
        # a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])


        file_name = '入库信息表{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("入库信息表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response


# 下载使用频率报表#mmm
@require_http_methods(['GET'])
def downUseFrequencyInfo(request):
    uPath = Utils.getUDiskPath()
    visitType = request.GET.get('visitType')
    if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
        retrunData = Utils.resultData(1, '未检测到U盘！')
        return JsonResponse(retrunData)
    search_dict = {
        "Name=": request.GET.get('searchValue', ''),
        "DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%M:%S') >=": request.GET.get('recordDateStart', ''),
        "DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%M:%S') <=": request.GET.get('recordDateEnd', '')
    }
    param_str = ''
    for key, value in search_dict.items():
        if search_dict[key] != '':
            param_str = param_str + "{0}'{1}' and ".format(key, value)
    if param_str != '':
        param_str = 'WHERE {0}'.format(param_str.strip(' and '))
    #     SQL = """
    #     SELECT b.Name, SUM(CASE WHEN a.RecordType=1 then 1 else 0 end) as TotalCount, b.Speci,
    #     min(DATE_FORMAT(a.CreateDate, '%Y-%m-%d %H:%i:%S')) as minTime,
    #     max(DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S'))as maxTime,
    #     SUM(CASE WHEN a.RecordType=2 then 1 else 0 end) as usedTimes,
    #     SUM(CASE WHEN a.RecordType=3 then 1 else 0 end) as returnTimes
    #     FROM rms_medicamentrecord as a RIGHT join rms_medicamentvariety as b on a.VarietyId=b.VarietyId
    #     {0} and a.VarietyId IS NOT NULL and b.VarietyId IS NOT NULL
    #     GROUP BY b.VarietyId;
    #     """.format(param_str)
    # else:
    #     SQL = """
    #     SELECT b.Name, SUM(CASE WHEN a.RecordType=1 then 1 else 0 end) as TotalCount, b.Speci,
    #     min(DATE_FORMAT(a.CreateDate, '%Y-%m-%d %H:%i:%S')) as minTime,
    #     max(DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S'))as maxTime,
    #     SUM(CASE WHEN a.RecordType=2 then 1 else 0 end) as usedTimes,
    #     SUM(CASE WHEN a.RecordType=3 then 1 else 0 end) as returnTimes
    #     FROM rms_medicamentrecord as a RIGHT join rms_medicamentvariety as b on a.VarietyId=b.VarietyId
    #     WHERE a.VarietyId IS NOT NULL and b.VarietyId IS NOT NULL
    #     GROUP BY b.VarietyId;
    #     """
        SQL = """
                       SELECT b.Name, SUM(CASE WHEN a.RecordType=1 then 1 else 0 end) as TotalCount, b.Speci,b.SpeciUnit,b.Purity,
                       min(DATE_FORMAT(a.CreateDate, '%Y-%m-%d %H:%i:%S')) as minTime,
                       max(DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S'))as maxTime, 
                       SUM(CASE WHEN a.RecordType=2 then 1 else 0 end) as usedTimes,
                       SUM(CASE WHEN a.RecordType=3 then 1 else 0 end) as returnTimes
                       FROM rms_medicamentrecord as a RIGHT join rms_medicamentvariety as b on a.VarietyId=b.VarietyId
                       {0}       
                       GROUP BY b.VarietyId;
                       """.format(param_str)
    else:
        SQL = """
                       SELECT b.Name, SUM(CASE WHEN a.RecordType=1 then 1 else 0 end) as TotalCount, b.Speci,b.SpeciUnit,b.Purity,
                       min(DATE_FORMAT(a.CreateDate, '%Y-%m-%d %H:%i:%S')) as minTime,
                       max(DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S'))as maxTime, 
                       SUM(CASE WHEN a.RecordType=2 then 1 else 0 end) as usedTimes,
                       SUM(CASE WHEN a.RecordType=3 then 1 else 0 end) as returnTimes
                       FROM rms_medicamentrecord as a RIGHT join rms_medicamentvariety as b on a.VarietyId=b.VarietyId      
                       GROUP BY b.VarietyId;
                       """
    drug_obj_list = BllMedicament().execute(SQL).fetchall()
    drug_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))
    # 创建一个报表类实例
    a = ReportData()
    a.set_style(title='Sheet')
    # 定义总共多少列
    data_list = ['品名', '纯度', '规格','剩余数量(瓶)', '起始时间', "终止时间", "领用次数", "归还次数"]
    # 写入第一行 第二行
    a.create_row1('使用频率统计表', len(data_list))

    # 写入第三行
    a.create_row3(data_list)
    # 写入有规律的多行数据
    keys_list = ['Name', 'Purity', 'Speci','TotalCount', 'minTime', 'maxTime', 'usedTimes', 'returnTimes']
    a.create_multiple_rows(4, drug_obj_list, keys_list)
    # 编辑空白替换为null
    a.replace_space(len(data_list))
    # 编辑试剂状态
    # a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
    # 编辑试剂重点监管
    # a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])
    file_name = '使用频率统计表{}'.format(Utils.getFileName())
    if(((visitType=='1') or (visitType=='2'))):
        a.save(uPath + '/' + file_name)
        retrunData = Utils.resultData(0, '导出成功')
        return JsonResponse(retrunData)
    else:
        a.save(file_name)
        response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
        response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        response['Content-Disposition'] = 'attachment;filename=' + urlquote("使用频率统计表.xls")  # 注意filename 这个是下载后的名字
        response.set_cookie('fileDownload', True, 1)
        return response


# 下载消耗统计报表
@require_http_methods(['GET'])
def downDrugConsumeInfo(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        search_dict = {
            'Name like ': '%'+request.GET.get('searchValue', '')+'%',
            "DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S') >=": request.GET.get('startDate', ''),
            "DATE_FORMAT(a.CreateDate,'%Y-%m-%d %H:%i:%S') <=": request.GET.get('endDate', '')
        }
        param_str = ''
        for key, value in search_dict.items():
            if search_dict[key] != '':
                param_str = param_str + "{0}'{1}' and ".format(key, value)
        if param_str != '':
            param_str = 'WHERE {0}'.format(param_str.strip(' and '))

        print(param_str)

        SQL_a = """SELECT  b.VarietyId as VarietyId, COUNT(CASE when IsEmpty = 1 then 1 end) as QuarterlyEmptyCount, 
                                             sum(CASE when IsEmpty = 1 then a.price else 0 end) as QuarterlyEmptyPrice,COUNT(CASE when RecordType = 1 then 1 end) as RecordType from RMS_MedicamentVariety  as b LEFT JOIN RMS_MedicamentRecord as a on
                                              b.VarietyId = a.VarietyId {0} GROUP by b.VarietyId""".format(param_str)
        print('下载第一ci记录', SQL_a)
        # 获取试剂消耗数据
        quarter_data = BllMedicamentVariety().execute(SQL_a).fetchall()
        quarter_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(quarter_data)))

        SQL = """
                           select  a.VarietyId as VarietyId, a.Name,a.Purity,a.CASNumber,a.IsSupervise, b.Price,
                           sum(case when b.`Status` = 1 then 1 else 0 end) as NormalCount,  
                           sum(case when b.`Status` = 1 or b.`Status` = 2 then 1 else 0 end) as TotalCount,
                           sum(case when b.`Status` = 2 then 1 else 0 end) as UseCount, 
                           sum(case when b.`Status` = 1 or b.`Status` = 2 then b.Price else 0 end)  as StockPrice 
                           from RMS_MedicamentVariety as a LEFT JOIN RMS_Medicament
                           as b on b.VarietyId = a.VarietyId GROUP BY a.VarietyId
                       """
        # 获取试剂数据
        med_data = BllMedicamentVariety().execute(SQL).fetchall()
        med_data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(med_data)))
        new_data_list = []
        # 遍历数据通过VarietyID相同合并字典
        for quarter in quarter_data:
            for med in med_data:
                if quarter['VarietyId'] == med['VarietyId']:
                    new_data = dict(quarter, **med)
                    new_data_list.append(new_data)

        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 总共多少列data_list的长度
        data_list = ['试剂类别', '纯度', 'CAS码', '重点监管', '当前库存总量', '当前在库数量', '当前借出数量', '当前库存价值(元)',
                     '入库数量', '消耗总量', "单价", '消耗总价值']
        # 写入第一行第二行
        a.create_row1('消耗统计信息报表', len(data_list))
        a.create_row3(data_list)
        keys_list = ['Name', 'Purity', 'CASNumber', 'IsSupervise', 'TotalCount', 'NormalCount', 'UseCount',
                     'StockPrice', 'RecordType', 'QuarterlyEmptyCount', 'Price', 'QuarterlyEmptyPrice', ]
        a.create_multiple_rows(4, new_data_list, keys_list)
        a.replace_space(len(keys_list))
        a.editor_isSupervise(string.ascii_uppercase[:14][keys_list.index('IsSupervise')])
        file_name = '消耗统计信息报表{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("消耗统计信息报表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response


# 下载保质期统计报表
def downShelflifeInfo(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        client_id = request.GET.get('client_id', '')
        searchValue = request.GET.get("searchValue", '')
        SQL_str = ''
        if searchValue:
            SQL_str = 'WHERE RMS_Medicament.Name = "{0}"'.format(searchValue.strip())

        if client_id and client_id != 'undefined':
            SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament where RMS_Medicament.ClientId" \
                  "=:client_id;"
            drug_obj_list = BllMedicament().execute(SQL, {'client_id': client_id}).fetchall()
        else:
            SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament {0} ORDER BY SurplusDays ASC;".format(SQL_str)
            drug_obj_list = BllMedicament().execute(SQL).fetchall()
        drug_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))
        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 定义总共多少列
        data_list = ['条形编号', '中文名称', '英文名称', 'CAS码', '纯度', '生产日期',
                     '剩余有效天数(天)', '试剂余量(g)', '生产商家', '经销商', ]
        # 写入第一行 第二行
        a.create_row1('当前保质期统计报表', len(data_list))

        # 写入第三行
        a.create_row3(data_list)
        # 写入有规律的多行数据
        keys_list = ['BarCode', 'Name', 'EnglishName', 'CASNumber', 'Purity',
                     'ProductionDate', 'SurplusDays', 'Remain',
                     'Manufacturer', 'Distributor']
        a.create_multiple_rows(4, drug_obj_list, keys_list)
        # 编辑空白替换为null
        a.replace_space(len(data_list))
        # # 编辑试剂状态
        # a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # # 编辑试剂重点监管
        # a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])


        file_name = '当前保质期统计报表{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("当前保质期统计报表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response


# 下载保质期预警统计报表
@require_http_methods(['GET'])
def downShelflifeWarning(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        warningDays = request.GET.get('WarningDays', '')

        if warningDays and warningDays != 'undefined':
            SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament where DATEDIFF(ExpirationDate,now())" \
                  "<:warningDays ORDER BY SurplusDays ASC;"
            drug_obj_list = BllMedicament().execute(SQL, {'warningDays': warningDays}).fetchall()
        else:
            SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament ORDER BY SurplusDays ASC;"
            drug_obj_list = BllMedicament().execute(SQL).fetchall()
        drug_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))
        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 定义总共多少列
        data_list = ['条形编号', '中文名称', '英文名称', 'CAS码', '纯度', '生产日期',
                     '剩余有效天数(天)', '试剂余量(g)', '生产商家', '经销商', ]
        # 写入第一行 第二行
        a.create_row1('保质期预警统计报表(小于{}天)'.format(warningDays), len(data_list))

        # 写入第三行
        a.create_row3(data_list)
        # 写入有规律的多行数据
        keys_list = ['BarCode', 'Name', 'EnglishName', 'CASNumber', 'Purity',
                     'ProductionDate', 'SurplusDays', 'Remain',
                     'Manufacturer', 'Distributor']
        a.create_multiple_rows(4, drug_obj_list, keys_list)
        # 编辑空白替换为null
        a.replace_space(len(data_list))
        # # 编辑试剂状态
        # a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # # 编辑试剂重点监管
        # a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])


        file_name = '保质期预警统计报表{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("保质期预警统计报表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response


# 下载库存呆滞表
@require_http_methods(['GET'])
def downStagnantInfo(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        client_id = request.GET.get('client_id', '')

        if client_id and client_id != 'undefined':
            SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament where RMS_Medicament.ClientId" \
                  "=:client_id;"
            drug_obj_list = BllMedicament().execute(SQL, {'client_id': client_id}).fetchall()
        else:
            SQL = "SELECT * FROM ( SELECT RMS_Medicament.*, DATEDIFF(ProductionDate,now()) as StagnantDays,Count(CASE when rms_medicamentrecord.RecordType != 1 then 1 end) AS useCount from RMS_Medicament " \
                  " LEFT JOIN rms_medicamentrecord ON RMS_Medicament.MedicamentId=rms_medicamentrecord.MedicamentId  ) as T WHERE T.useCount=0  ORDER BY T.StagnantDays DESC LIMIT 20;"
            drug_obj_list = BllMedicament().execute(SQL).fetchall()
        drug_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))
        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 定义总共多少列
        data_list = ['条形编号', '中文名称', '英文名称', 'CAS码', '纯度', '生产日期',
                     '呆滞时长(天)', '试剂余量(g)', '生产商家', '经销商', ]
        # 写入第一行 第二行
        a.create_row1('库存呆滞统计报表', len(data_list))

        # 写入第三行
        a.create_row3(data_list)
        # 写入有规律的多行数据
        keys_list = ['BarCode', 'Name', 'EnglishName', 'CASNumber', 'Purity',
                     'ProductionDate', 'StagnantDays', 'Remain',
                     'Manufacturer', 'Distributor']
        a.create_multiple_rows(4, drug_obj_list, keys_list)
        # 编辑空白替换为null
        a.replace_space(len(data_list))
        # # 编辑试剂状态
        # a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # # 编辑试剂重点监管
        # a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])


        file_name = '库存呆滞统计报表{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("库存呆滞统计报表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response


# 下载试剂历史使用表
@require_http_methods(['GET'])
def downDrugUseRecordInfo(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        client_id = request.GET.get('client_id', '')
        search_val = request.GET.get('search_val', '')
        startDate = request.GET.get('startDate', '')
        endDate = request.GET.get('endDate', '')
        recordtype_val = request.GET.get('recordtype_val', '')
        str1 = ""
        #mxh_获取查询到的数据
        report_record_list = DrugUseRecordInfoSelect(client_id, search_val, startDate, endDate, recordtype_val)

        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        data_list = ['条形编号', 'CAS码', '中文名称', '英文名称', '纯度', '用量', '操作人员', '操作类型', '目前状态',
                     '所属柜号', '记录日期', ]
        a.create_row1('试剂历史使用记录报表', len(data_list))
        a.create_row3(data_list)
        keys_list = ['BarCode', 'CASNumber', 'Name', 'EnglishName', 'Purity','UseQuantity', 'CreateUserName', 'RecordType',
                     'Status', 'ClientCode', 'CreateDate', ]
        a.create_multiple_rows(4, report_record_list, keys_list)
        a.editor_time(keys_list, 'CreateDate')
        a.replace_space(len(data_list))
        # 编辑试剂状态 string.ascii_uppercase[keys_list.index('Status')] 获取状态的列数
        a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # 编辑试剂类型
        a.editor_RecordType(string.ascii_uppercase[keys_list.index('RecordType')])
        file_name = '试剂历史使用记录报表{}'.format(Utils.getFileName())
        # print('试剂保存名称：',file_name)
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("试剂历史使用记录报表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response

#mxh_根据时间，搜索条件，归还类型...查询试剂历史使用记录数据库
def DrugUseRecordInfoSelect(client_id, search_val, startDate, endDate, recordtype_val):
    print('试剂处理下载数据', client_id, search_val, startDate, endDate, recordtype_val)
    if client_id:
        if search_val:
            if startDate:
                if endDate:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_Medicament.BarCode like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate BETWEEN :startDate AND :endDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_Medicament.BarCode like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate BETWEEN :startDate AND :endDate) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                else:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_Medicament.BarCode like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate>:startDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_Medicament.BarCode like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate>:startDate) ORDER BY RMS_MedicamentRecord.CreateDate desc"
            else:
                if endDate:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_Medicament.BarCode like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate<:endDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_Medicament.BarCode like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate<:endDate) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                else:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_Medicament.BarCode like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_Medicament.BarCode like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) ORDER BY RMS_MedicamentRecord.CreateDate desc"
        else:
            if startDate:
                if endDate:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_MedicamentRecord.CreateDate BETWEEN :startDate AND :endDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_MedicamentRecord.CreateDate BETWEEN :startDate AND :endDate) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                else:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_MedicamentRecord.CreateDate>:startDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_MedicamentRecord.CreateDate>:startDate) ORDER BY RMS_MedicamentRecord.CreateDate desc"
            else:
                if endDate:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_MedicamentRecord.CreateDate<:endDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_MedicamentRecord.CreateDate<:endDate) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                else:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.ClientId = :client_id) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE RMS_Medicament.ClientId = :client_id ORDER BY RMS_MedicamentRecord.CreateDate desc"
    else:
        if search_val:
            if startDate:
                if endDate:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.BarCode like :search_val or RMS_Medicament.CASNumber like :search_val or RMS_Medicament.Name like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate BETWEEN :startDate AND :endDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE (RMS_Medicament.BarCode like :search_val or RMS_Medicament.CASNumber like :search_val or RMS_Medicament.Name like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate BETWEEN :startDate AND :endDate) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                else:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.BarCode like :search_val or RMS_Medicament.CASNumber like :search_val or RMS_Medicament.Name like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate>:startDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE (RMS_Medicament.BarCode like :search_val or RMS_Medicament.CASNumber like :search_val or RMS_Medicament.Name like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate>:startDate) ORDER BY RMS_MedicamentRecord.CreateDate desc"
            else:
                if endDate:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.BarCode like :search_val or RMS_Medicament.CASNumber like :search_val or RMS_Medicament.Name like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate<:endDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE (RMS_Medicament.BarCode like :search_val or RMS_Medicament.CASNumber like :search_val or RMS_Medicament.Name like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.CreateDate<:endDate) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                else:
                    if recordtype_val:
                        str1 = " WHERE (RMS_Medicament.BarCode like :search_val or RMS_Medicament.CASNumber like :search_val or RMS_Medicament.Name like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE RMS_Medicament.BarCode like :search_val or RMS_Medicament.CASNumber like :search_val or RMS_Medicament.Name like :search_val or RMS_MedicamentRecord.CreateUserName like :search_val ORDER BY RMS_MedicamentRecord.CreateDate desc"
        else:
            if startDate:
                if endDate:
                    if recordtype_val:
                        str1 = " WHERE (RMS_MedicamentRecord.CreateDate BETWEEN :startDate AND :endDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE RMS_MedicamentRecord.CreateDate BETWEEN :startDate AND :endDate ORDER BY RMS_MedicamentRecord.CreateDate desc"
                else:
                    if recordtype_val:
                        str1 = " WHERE (RMS_MedicamentRecord.CreateDate>:startDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE RMS_MedicamentRecord.CreateDate>:startDate ORDER BY RMS_MedicamentRecord.CreateDate desc"
            else:
                if endDate:
                    if recordtype_val:
                        str1 = " WHERE (RMS_MedicamentRecord.CreateDate<:endDate) and (RMS_MedicamentRecord.RecordType=:RecordType) ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " WHERE RMS_MedicamentRecord.CreateDate<:endDate ORDER BY RMS_MedicamentRecord.CreateDate desc"
                else:
                    if recordtype_val:
                        str1 = " WHERE RMS_MedicamentRecord.RecordType=:RecordType ORDER BY RMS_MedicamentRecord.CreateDate desc"
                    else:
                        str1 = " ORDER BY RMS_MedicamentRecord.CreateDate desc"
    SQL1 = "SELECT CreateDate,RecordType, RMS_Medicament.EnglishName, RMS_Medicament.Name, " \
           "RMS_Medicament.BarCode, RMS_Medicament.ByUserName, RMS_Medicament.Purity, RMS_Medicament." \
           "`Status`, RMS_Medicament.Place,RMS_MedicamentRecord.RecordRemain,RMS_MedicamentRecord.UseQuantity,RMS_MedicamentRecord.ClientCode, RMS_MedicamentRecord.CreateUserName, PutInUserName, CASNumber FROM `RMS_MedicamentRecord` INNER JOIN " \
           " RMS_Medicament ON RMS_MedicamentRecord.MedicamentId = RMS_Medicament.MedicamentId"
    SQL = SQL1 + str1
    report_record_list = BllMedicamentRecord().execute(SQL, {'client_id': client_id, 'search_val':'%'+search_val+'%',
                                                             'startDate': startDate, 'endDate': endDate,
                                                             'RecordType': recordtype_val}).fetchall()
    report_record_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(report_record_list)))
    return report_record_list


# 下载人员用量统计报表
@require_http_methods(['GET'])
def downUserConsumeInfo(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        client_id = request.GET.get('client_id', '')

        if client_id and client_id != 'undefined':
            SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament where RMS_Medicament.ClientId" \
                  "=:client_id;"
            drug_obj_list = BllMedicament().execute(SQL, {'client_id': client_id}).fetchall()
        else:
            SQL = "SELECT * FROM ( SELECT RMS_Medicament.*, DATEDIFF(ProductionDate,now()) as StagnantDays,Count(CASE when rms_medicamentrecord.RecordType != 1 then 1 end) AS useCount from RMS_Medicament " \
                  " LEFT JOIN rms_medicamentrecord ON RMS_Medicament.MedicamentId=rms_medicamentrecord.MedicamentId  ) as T WHERE T.useCount=0  ORDER BY T.StagnantDays DESC LIMIT 20;"
            drug_obj_list = BllMedicament().execute(SQL).fetchall()
        drug_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))
        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 定义总共多少列
        data_list = ['条形编号', '中文名称', '英文名称', 'CAS码', '纯度', '生产日期',
                     '呆滞时长(天)', '试剂余量(g)', '生产商家', '经销商', ]
        # 写入第一行 第二行
        a.create_row1('库存呆滞统计报表', len(data_list))

        # 写入第三行
        a.create_row3(data_list)
        # 写入有规律的多行数据
        keys_list = ['BarCode', 'Name', 'EnglishName', 'CASNumber', 'Purity',
                     'ProductionDate', 'StagnantDays', 'Remain',
                     'Manufacturer', 'Distributor']
        a.create_multiple_rows(4, drug_obj_list, keys_list)
        # 编辑空白替换为null
        a.replace_space(len(data_list))
        # # 编辑试剂状态
        # a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # # 编辑试剂重点监管
        # a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])


        file_name = '库存呆滞统计报表{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("库存呆滞统计报表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response


# 下载试剂种类消耗统计报表
@require_http_methods(['GET'])
def downDrugUseCategotyConsumeInfo(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        client_id = request.GET.get('client_id', '')

        if client_id and client_id != 'undefined':
            SQL = "SELECT *, DATEDIFF(ExpirationDate,now()) as SurplusDays from RMS_Medicament where RMS_Medicament.ClientId" \
                  "=:client_id;"
            drug_obj_list = BllMedicament().execute(SQL, {'client_id': client_id}).fetchall()
        else:
            SQL = "SELECT * FROM ( SELECT RMS_Medicament.*, DATEDIFF(ProductionDate,now()) as StagnantDays,Count(CASE when rms_medicamentrecord.RecordType != 1 then 1 end) AS useCount from RMS_Medicament " \
                  " LEFT JOIN rms_medicamentrecord ON RMS_Medicament.MedicamentId=rms_medicamentrecord.MedicamentId  ) as T WHERE T.useCount=0  ORDER BY T.StagnantDays DESC LIMIT 20;"
            drug_obj_list = BllMedicament().execute(SQL).fetchall()
        drug_obj_list = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(drug_obj_list)))
        # 创建一个报表类实例
        a = ReportData()
        a.set_style(title='Sheet')
        # 定义总共多少列
        data_list = ['条形编号', '中文名称', '英文名称', 'CAS码', '纯度', '生产日期',
                     '呆滞时长(天)', '试剂余量(g)', '生产商家', '经销商', ]
        # 写入第一行 第二行
        a.create_row1('库存呆滞统计报表', len(data_list))

        # 写入第三行
        a.create_row3(data_list)
        # 写入有规律的多行数据
        keys_list = ['BarCode', 'Name', 'EnglishName', 'CASNumber', 'Purity',
                     'ProductionDate', 'StagnantDays', 'Remain',
                     'Manufacturer', 'Distributor']
        a.create_multiple_rows(4, drug_obj_list, keys_list)
        # 编辑空白替换为null
        a.replace_space(len(data_list))
        # # 编辑试剂状态
        # a.editor_status(string.ascii_uppercase[keys_list.index('Status')])
        # # 编辑试剂重点监管
        # a.editor_isSupervise(string.ascii_uppercase[keys_list.index('IsSupervise')])


        file_name = '库存呆滞统计报表{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            a.save(file_name)
            response = StreamingHttpResponse(ReportData.download_excel(filename=file_name + '.xlsx'))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote("库存呆滞统计报表.xls")  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response