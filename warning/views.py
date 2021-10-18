import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

# from Lib.Utils import logger
from Business.BllWarning import *


# 获取预警数量
@require_http_methods(['GET'])
def warning_numbers(request):
    if request.method == 'GET':
        SQL = 'SELECT count(*) as number_ FROM `RMS_Warning` WHERE IsSolve = 0 and now() > WarningDate;'
        warning_obj = BllWarning().execute(SQL).fetchone()
        warning_nb = warning_obj.number_
        return JsonResponse({'number': warning_nb})


# 获取预警管理页面
@require_http_methods(['GET'])
def index(request):
    if request.method == 'GET':
        searchValue = request.GET.get('searchValue', '')
        tag = request.GET.get('tag', 0)
        today = (date.today() + relativedelta.relativedelta(days=1)).strftime('%Y-%m-%d')
        last_year = (date.today() + relativedelta.relativedelta(years=-1, days=1)).strftime('%Y-%m-%d')
        return render(request, 'warning/index.html', locals())


# 获取预警Json数据
@require_http_methods(['GET'])
def getWarningListJson(request):
    if request.method == 'GET':
        searchValue = request.GET.get('searchValue', '')
        if not searchValue:
            warning_list = BllWarning().findList().order_by(desc(EntityWarning.IsSolve), desc(EntityWarning.WarningDate), desc(EntityWarning.SolveDate)).all()
            return JsonResponse({'data': json.loads (Utils.resultAlchemyData(warning_list))})
        else:
            warning_list = BllWarning().like_warning_list(searchValue)
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(warning_list))})


# 查看预警管理详情
@require_http_methods(['GET'])
def form(request):
    if request.method == 'GET':
        WarningId = request.GET.get('warning_id')
        if WarningId:
            Warning_obj = BllWarning().findEntity(WarningId)
            return render(request, 'warning/form.html', locals())
        else:
            return render(request, 'warning/form.html', {'data': '数据异常'})


# 保存预警管理
@require_http_methods(['POST'])
@csrf_exempt
def solveWarning(request):
    if request.method == 'POST':
        WarningId = request.POST.get('WarningId', '')
        IsSolve = request.POST.get('IsSolve', '')
        SolveDate = request.POST.get('SolveDate', '')
        SolveDate = datetime.datetime.strptime(SolveDate, '%Y-%m-%d')
        SolveContent = request.POST.get('SolveContent', '')
        if IsSolve == '0' or not IsSolve:
            return JsonResponse(Utils.resultData('0', '保存失败, 是否解决没被选中'))
        warning_obj = BllWarning().findEntity(WarningId)
        warning_obj.IsSolve = 1
        warning_obj.SolveDate = SolveDate
        warning_obj.SolveUserName = request.session['login_user']['RealName']
        warning_obj.SolveUserId = request.session['login_user']['UserId']
        warning_obj.SolveContent = SolveContent
        BllWarning().update(warning_obj)
        return JsonResponse(Utils.resultData('1', '保存成功', ''))
