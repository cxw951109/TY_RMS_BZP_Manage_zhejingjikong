from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Business.BllClient import *
from Business.BllClientUser import *
from Business.BllUser import *
from Business.BllMedicament import *
from Business.BllMedicamentRecord import *

from DataEntity.EntityMedicamentRecord import *
from Lib.Utils import *
from Lib.Model import *

# 获取试剂列表Json数据
@require_http_methods(['GET'])
@csrf_exempt
def getDrugList(request):
    if request.method == 'GET':
        name = request.GET.get("searchValue", '')
        curPage = int(request.GET.get("curPage", 1))
        pageSize =int(request.GET.get("pageSize", 10))
        drug_list = BllMedicament().getAllDrugList(name, PageParam(curPage, pageSize))
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(drug_list)),'message':'成功','status':0})

# 获取用户列表Json数据
@require_http_methods(['GET'])
@csrf_exempt
def getUserList(request):
    if request.method == 'GET':
        searchValue = request.GET.get('searchValue', '')
        curPage = int(request.GET.get("curPage", 1))
        pageSize =int(request.GET.get("pageSize", 10))
        queryOrm = BllUser().findList()
        data=BllUser().queryPage(queryOrm,PageParam(curPage, pageSize))
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'message':'成功','status':0})


# 获取用户流转记录Json数据
@require_http_methods(['GET'])
@csrf_exempt
def getDrugRecordList(request):
    if request.method == 'GET':
        searchValue = request.GET.get('userRealName', '')
        curPage = int(request.GET.get("curPage", 1))
        pageSize =int(request.GET.get("pageSize", 10))
        print(searchValue)
        queryOrm = None
        if not searchValue:
            queryOrm = BllMedicamentRecord().findList()
        else:
            queryOrm = BllMedicamentRecord().findList(EntityMedicamentRecord.CreateUserName==searchValue)
        data=BllMedicamentRecord().queryPage(queryOrm,PageParam(curPage, pageSize))
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'message':'成功','status':0})
