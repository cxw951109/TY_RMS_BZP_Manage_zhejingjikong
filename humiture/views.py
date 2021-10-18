import json
from dateutil.relativedelta import relativedelta
from datetime import date
import time
from sqlalchemy import func

from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.http import urlquote

from Business.BllHumitureRecord import *
from Business.BllClient import *
from Lib.Utils import *
from DataEntity.EntityHumitureRecord import *
from Lib.reportExcel import *


@require_http_methods(['GET'])
def index(request):
    if request.method == 'GET':
        today = (date.today() + relativedelta.relativedelta(days=1)).strftime('%Y-%m-%d')
        last_year = (date.today() + relativedelta.relativedelta(years=-1, days=1)).strftime('%Y-%m-%d')
        return render(request, 'humiture/index.html', locals())


# 获取温湿度Json数据
@require_http_methods(['GET'])
def getHumitureListJson(request):
    if request.method == 'GET':
        try:
            humiture_type = request.GET.get('type')
            # 判断是否传参  没有传参默认 humiture_type = '1'
            if not humiture_type or humiture_type == '1':
                startData = request.GET.get('startDate', '')
                endData = request.GET.get('endDate', '')
                # 搜索框的值
                searchValue = request.GET.get('searchValue', '')
                # ajax传过来的参数
                params = json.loads(request.GET.get('params', ''))
                startIndex = params['startIndex']
                pageSize = params['pageSize']

                page = params['page']
                # 实例化一个对象
                pageParam = PageParam(curPage=page, pageRows=pageSize, orderType=desc)
                data = BllHumitureRecord().queryPage(BllHumitureRecord().findList(and_(EntityHumitureRecord.RecordDate >= startData,
                                                                                        EntityHumitureRecord.RecordDate <= endData)).order_by(desc(EntityHumitureRecord.RecordDate)), pageParam)
                return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)), 'total': pageParam.totalRecords})

        except:
            BllHumitureRecord().session.rollback()
        finally:
            BllHumitureRecord().session.close()

# 获取温湿度Json数据(按天平均值)
@require_http_methods(['GET'])
def getHumitureListJson1(request):
    if request.method == 'GET':
        try:
            startDate = request.GET.get('startDate', '')
            endDate = request.GET.get('endDate', '')
            # 搜索框的值
            searchValue = request.GET.get('searchValue', '')
            SQL = "select *, ROUND(AVG(Temperature),1) as avgTemp,DATE_FORMAT(RecordDate,'%Y-%m-%d') as avgDate  from rms_humiturerecord "
            SQL+=' Where 1=1 '
            param={}
            if(startDate!=''):
                SQL+=' and RecordDate>:startDate '
                param['startDate']=startDate
            if(endDate!=''):
                SQL+=' and RecordDate<:endDate '
                param['endDate']=endDate
            SQL+=" GROUP BY DATE_FORMAT(RecordDate,'%Y-%m-%d') ORDER BY avgDate DESC;"
            data = BllHumitureRecord().execute(SQL,param).fetchall()
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(data)))})
        except Exception as e:
            logger.debug('数据库操作失败',str(e))
            BllHumitureRecord().session.rollback()
        finally:
            BllHumitureRecord().session.close()
    # if request.method == 'GET':
    #     try:
    #         humiture_type = request.GET.get('type')
    #         # 判断是否传参  没有传参默认 humiture_type = '1'
    #         if not humiture_type or humiture_type == '1':
    #             startData = request.GET.get('startDate', '')
    #             endData = request.GET.get('endDate', '')
    #             # 搜索框的值
    #             searchValue = request.GET.get('searchValue', '')
    #             # ajax传过来的参数
    #             params = json.loads(request.GET.get('params', ''))
    #             startIndex = params['startIndex']
    #             pageSize = params['pageSize']

    #             page = params['page']
    #             # 实例化一个对象
    #             pageParam = PageParam(curPage=page, pageRows=pageSize, orderType=desc)
    #             data = BllHumitureRecord().queryPage(BllHumitureRecord().findList(and_(EntityHumitureRecord.RecordDate >= startData,
    #                                                                                     EntityHumitureRecord.RecordDate <= endData)).order_by(desc(EntityHumitureRecord.RecordDate)), pageParam)
    #             return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)), 'total': pageParam.totalRecords})

    #     except:
    #         BllHumitureRecord().session.rollback()
    #     finally:
    #         BllHumitureRecord().session.close()


# 获取温湿度静态展示数据
@require_http_methods(['GET'])
def getHumitureStatisticsJson(request):
    if request.method == 'GET':
        humiture_type = request.GET.get('type')
        # 判断是否传参  没有传参默认 humiture_type = '1'
        if not humiture_type or humiture_type == '1':
            data = Utils().get_temperature_or_humidity()
            return JsonResponse(Utils.resultData('1', '数据获取成功', data=data))

        else:
            # 传参则代表获取湿度
            data = Utils().get_temperature_or_humidity(params=1)
            return JsonResponse(Utils.resultData('1', '数据获取成功', data=data))


# 导出温湿度记录报表处理函数
@require_http_methods(['GET'])
def exportHumitureData(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)

        startData = request.GET.get('startDate', '')
        endData = request.GET.get('endDate', '')
        data = BllHumitureRecord().findList(and_(EntityHumitureRecord.RecordDate >= startData,
        EntityHumitureRecord.RecordDate <= endData)).order_by(desc(EntityHumitureRecord.RecordDate)).all()
        data = json.loads(Utils.resultAlchemyData(data))
        # 实例化一个报表类
        data_list = ['记录时间', '温度', '药柜名称']
        keys_list = ['RecordDate', 'Temperature', 'ClientName']
        a = ReportData()
        a.set_style(title='Sheet')
        # 创建第一行
        # 合并第1行1-14列单元格
        a.ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=len(keys_list))
        # 写入值
        a.ws.cell(row=1, column=1).value = '温度记录报表'
        a.ws['A1'].alignment = a.alignment_style
        a.ws['A1'].font = Font(size=16, bold=True)
        a.ws['A1'].border = a.border_style
        # 创建第二行
        # 第2行写入值
        now_time = datetime.datetime.now().strftime('%Y%m%d %H%M')
        # 格式化时间为中文年月日
        now_time = now_time[:4] + '年' + now_time[4:6] + '月' + now_time[6:8] + '日' + now_time[8:11] + '时' + now_time[
                                                                                                        11:13] + '分'
        a.ws.cell(row=2, column=1).value = '报表导出时间：{}'.format(now_time)
        a.ws.cell(row=2, column=2).value = '后台系统版本：Light_OS_Back_ver1.04'
        a.ws.cell(row=2, column=3).value = '终端系统版本:Light_OS_Front_ver1.06'
        a.ws.cell(row=2, column=4).value = '报表导出位置：后台'
        # 遍历一共多少列为每一列添加样式
        for x in range(1, len(keys_list) + 1):
            a.ws.cell(row=2, column=x).alignment = a.alignment_style
            a.ws.cell(row=2, column=x).font = a.font_size
            a.ws.cell(row=2, column=x).border = a.border_style
        # 创建第三行
        a.create_row3(data_list)
        # 创建多行
        a.create_multiple_rows(4, data, keys_list)
        a.editor_time(keys_list, 'RecordDate')
        a.replace_space(len(keys_list))
        # 随机生成一个文件后缀名
        save_file_name = 'HumitureExportTem{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + save_file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            file_path = save_file_name + '.xlsx'
            a.save(save_file_name)
            response = StreamingHttpResponse(ReportData.download_excel(file_path))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            # django自带一个urlquote函数用于url编码，解决不支持中文编码问题
            response['Content-Disposition'] = 'attachment;filename="{}.xlsx"'.format(urlquote('温度记录报表'))  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response


# 导出温湿度记录报表处理函数
@require_http_methods(['GET'])
def exportHumitureData1(request):
    if request.method == 'GET':
        uPath = Utils.getUDiskPath()
        visitType = request.GET.get('visitType')
        if (uPath == '' and ((visitType=='1') or (visitType=='2'))):
            retrunData = Utils.resultData(1, '未检测到U盘！')
            return JsonResponse(retrunData)
        startDate = request.GET.get('startDate', '')
        endDate = request.GET.get('endDate', '')
        # 搜索框的值
        searchValue = request.GET.get('searchValue', '')
        SQL = "select *, ROUND(AVG(Temperature),1) as avgTemp,DATE_FORMAT(RecordDate,'%Y-%m-%d') as avgDate  from rms_humiturerecord "
        SQL+=' Where 1=1 '
        param={}
        if(startDate!=''):
            SQL+=' and RecordDate>:startDate '
            param['startDate']=startDate
        if(endDate!=''):
            SQL+=' and RecordDate<:endDate '
            param['endDate']=endDate
        SQL+=" GROUP BY DATE_FORMAT(RecordDate,'%Y-%m-%d') ORDER BY avgDate DESC;"
        data = BllHumitureRecord().execute(SQL,param).fetchall()
        data = json.loads(Utils.resultAlchemyData(Utils.mysqlTable2Model(data)))
        # 实例化一个报表类
        data_list = ['记录时间', '温度','药柜名称']
        keys_list = ['RecordDate', 'avgTemp', 'ClientName']
        a = ReportData()
        a.set_style(title='Sheet')
        # 创建第一行
        # 合并第1行1-14列单元格
        a.ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=len(keys_list))
        # 写入值
        a.ws.cell(row=1, column=1).value = '温度记录报表'
        a.ws['A1'].alignment = a.alignment_style
        a.ws['A1'].font = Font(size=16, bold=True)
        a.ws['A1'].border = a.border_style
        # 创建第二行
        # 第2行写入值
        now_time = datetime.datetime.now().strftime('%Y%m%d %H%M')
        # 格式化时间为中文年月日
        now_time = now_time[:4] + '年' + now_time[4:6] + '月' + now_time[6:8] + '日' + now_time[8:11] + '时' + now_time[
                                                                                                           11:13] + '分'
        a.ws.cell(row=2, column=1).value = '报表导出时间：{}'.format(now_time)
        a.ws.cell(row=2, column=2).value = '后台系统版本：Light_OS_Back_ver1.04'
        a.ws.cell(row=2, column=3).value = '终端系统版本:Light_OS_Front_ver1.06'
        a.ws.cell(row=2, column=4).value = '报表导出位置：后台'
        # 遍历一共多少列为每一列添加样式
        for x in range(1, len(keys_list) + 1):
            a.ws.cell(row=2, column=x).alignment = a.alignment_style
            a.ws.cell(row=2, column=x).font = a.font_size
            a.ws.cell(row=2, column=x).border = a.border_style
        # 创建第三行
        a.create_row3(data_list)
        # 创建多行
        a.create_multiple_rows(4, data, keys_list)
        a.editor_time(keys_list, 'RecordDate')
        a.replace_space(len(keys_list))
        # 随机生成一个文件后缀名
        save_file_name = 'HumitureExportTem{}'.format(Utils.getFileName())
        if(((visitType=='1') or (visitType=='2'))):
            a.save(uPath + '/' + save_file_name)
            retrunData = Utils.resultData(0, '导出成功')
            return JsonResponse(retrunData)
        else:
            file_path = save_file_name + '.xlsx'
            a.save(save_file_name)
            response = StreamingHttpResponse(ReportData.download_excel(file_path))
            response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
            # django自带一个urlquote函数用于url编码，解决不支持中文编码问题
            response['Content-Disposition'] = 'attachment;filename="{}.xlsx"'.format(urlquote('温度记录报表'))  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response





