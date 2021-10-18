from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import json

from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote

from Business.BllLog import *
from DataEntity.EntityLog import *
from Lib.Utils import *
from Lib.reportExcel import *
from Lib.Model import PageParam


@require_http_methods(['GET'])
def index(request):
    if request.method == 'GET':
        # 获取当前日期
        today = (date.today() + relativedelta.relativedelta(days=1)).strftime('%Y-%m-%d')
        # 获取昨天的日期
        # yesterday = (date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
        last_year = (datetime.datetime.now() + relativedelta.relativedelta(years=-1, days=1)).strftime('%Y-%m-%d')
        searchValue = request.GET.get('searchValue', '')
        return render(request, 'log/index.html', locals())


@require_http_methods(['GET'])
def getLogListJson(request):
    if request.method == 'GET':
        # 起止时间
        startData =  request.GET.get('startDate', '')
        endData =  request.GET.get('endDate', '')
        # 搜索框的值
        searchValue = request.GET.get('searchValue', '')
        # ajax传过来的参数
        params = json.loads(request.GET.get('params', ''))
        startIndex = params['startIndex']
        pageSize = params['pageSize']
        page = params['page']
        # 实例化一个对象
        pageParam = PageParam(page, pageSize)
        if searchValue:
            data_list = BllLog().queryPage(BllLog().like_Log_data(searchValue).filter(and_(EntityLog.OperateDate > startData, EntityLog.OperateDate < endData)).order_by(desc(EntityLog.OperateDate)), pageParam)
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data_list)), 'total': pageParam.totalRecords})
        data = BllLog().queryPage(BllLog().findList(and_(EntityLog.OperateDate >= startData, EntityLog.OperateDate <= endData)).order_by(desc(EntityLog.OperateDate)), pageParam)

        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)), 'total': pageParam.totalRecords})


@require_http_methods(['GET'])
def exportLogData(request):
    if request.method == 'GET':
        data = BllLog().findList().order_by(desc(EntityLog.OperateDate)).all()
        data = json.loads(Utils.resultAlchemyData(data))
        # 实例化一个报表类
        data_list = ['操作时间', '操作用户', '操作类型', '操作内容']
        keys_list = ['OperateDate', 'OperateUserName', 'OperateType', 'ExecuteResult']
        a = ReportData()
        a.set_style(title='Sheet')
        # 创建第一行
        # 合并单元格
        a.ws.merge_cells(start_row=1, end_row=1, start_column=1, end_column=len(keys_list))
        # 写入值
        a.ws.cell(row=1, column=1).value = '操作日志报表'
        a.ws['A1'].alignment = a.alignment_style
        a.ws['A1'].font = Font(size=16, bold=True)
        a.ws['A1'].border = a.border_style
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
        a.create_row3(data_list)
        a.create_multiple_rows(4, data, keys_list)
        a.editor_time(keys_list, 'OperateDate')

        save_file_name = 'LogExportTmp{}'.format(Utils.UUID())
        a.save(save_file_name)
        file_path = save_file_name + '.xlsx'
        response = StreamingHttpResponse(ReportData.download_excel(file_path))
        response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        # django自带一个urlquote函数用于url编码，解决不支持中文编码问题
        response['Content-Disposition'] = 'attachment;filename="{}.xlsx"'.format(urlquote('操作日志报表'))  # 注意filename 这个是下载后的名字
        # 设置cookie让前端指定文件下载完成
        response.set_cookie('fileDownload', True, 1)
        return response
