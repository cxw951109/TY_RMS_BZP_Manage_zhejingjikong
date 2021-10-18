from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import json

from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote

from DataEntity.EntityApproveInfo import *
from DataEntity.EntityApproveInfoProcess import *
from DataEntity.EntityApproveType import *
from DataEntity.EntityApproveTypeProcess import *
from Business.BllApproveInfo import *
from Business.BllApproveType import *
from Business.BllApproveInfoProcess import *
from Business.BllApproveTypeProcess import *
from Business.BllUser import *

from Lib.Utils import *
from Lib.reportExcel import *
from Lib.Model import PageParam

@require_http_methods(['GET'])
def setIndex(request):
    if request.method == 'GET':
        return render(request, 'approve/setIndex.html', locals())

@require_http_methods(['GET'])
def mySend(request):
    if request.method == 'GET':
        return render(request, 'approve/mySend.html', locals())

@require_http_methods(['GET'])
def myReceive(request):
    if request.method == 'GET':
        return render(request, 'approve/myReceive.html', locals())

@require_http_methods(['GET'])
def setForm(request):
    if request.method == 'GET':
        ApproveTypeId= request.GET.get("ApproveTypeId",'')
        approve=BllApproveType().findEntity(ApproveTypeId)
        approve_type_list=[x.ObjectId for x in BllApproveTypeProcess().getTypeProcess(ApproveTypeId)] 
        all_user_list=BllUser().getSelectUserList()
        return render(request, 'approve/setForm.html', locals())

@require_http_methods(['GET'])
def approveForm(request):
    if request.method == 'GET':
        ApproveInfoId= request.GET.get("ApproveInfoId",'')
        model=BllApproveInfo().findEntity(ApproveInfoId)
        approve_info_process_list=BllApproveInfoProcess().getApproveInfoProcess(ApproveInfoId)
        return render(request, 'approve/approveForm.html', locals())

@require_http_methods(['GET'])
def approveView(request):
    if request.method == 'GET':
        ApproveInfoId= request.GET.get("ApproveInfoId",'')
        model=BllApproveInfo().findEntity(ApproveInfoId)
        approve_info_process_list=BllApproveInfoProcess().getApproveInfoProcess(ApproveInfoId)
        return render(request, 'approve/approveView.html', locals())



# 获取审批类型列表Json数据
@require_http_methods(['GET'])
def getApproveTypeListJson(request):
    if request.method == 'GET':
        SQL="""
        SELECT a.*,GROUP_CONCAT(CONCAT(c.RealName,'(',c.UserCode,')')  ORDER BY b.SortIndex ASC separator '=>') AS ApproveTypeProcess
        FROM rms_approvetype a LEFT JOIN rms_approvetypeprocess b ON a.ApproveTypeId=b.ApproveTypeId 
        LEFT JOIN rms_user c ON b.ObjectId=c.UserId  GROUP BY a.ApproveTypeId ORDER BY a.CreateDate DESC
        """
        type_list = BllApproveType().execute(SQL).fetchall()
        type_list = Utils.mysqlTable2Model(type_list)
        data = type_list
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':10000})


# 获取我申请的审批信息列表Json数据
@require_http_methods(['GET'])
def getMySendApproveInfoListJson(request):
    if request.method == 'GET':
        ApproveInfoCode = request.GET.get('ApproveInfoCode', '')
        ApproveCurAcceptUserName = request.GET.get('ApproveCurAcceptUserName', '')
        ApproveTypeCode = request.GET.get('ApproveTypeCode', '')
        ApproveStatus = request.GET.get('ApproveStatus', '')
        curPage = int(request.GET.get('page', '1'))
        pageSize = int(request.GET.get('limit', '10'))
        pageParam = PageParam(curPage,pageSize)
        user_ = request.session['login_user']
        SQL="""
        SELECT * FROM( SELECT a.*,GROUP_CONCAT(CONCAT(c.RealName,'(',c.UserCode,')')  ORDER BY b.SortIndex ASC separator '=>') AS ApproveInfoProcess
        FROM rms_approveinfo a LEFT JOIN rms_approveinfoprocess b ON a.ApproveInfoId=b.ApproveInfoId 
        LEFT JOIN rms_user c ON b.ApproveUserId=c.UserId  GROUP BY a.ApproveInfoId ORDER BY a.CreateDate DESC ) nt WHERE CreateUserId='"""+user_['UserId']+"""'
        """
        if(ApproveInfoCode):
            SQL+= " and ApproveInfoCode like '%"+ApproveInfoCode+"%'"
        if(ApproveCurAcceptUserName):
            SQL+= " and ApproveCurAcceptUserName like '%"+ApproveCurAcceptUserName+"%'"
        if(ApproveTypeCode):
            SQL+=" and ApproveTypeCode = '"+ApproveTypeCode+"'"
        if(ApproveStatus):
            SQL+=" and ApproveStatus = "+ApproveStatus
        queryParams={}
        info_list=BllApproveInfo().execute(SQL+ ' limit '+ str((pageParam.curPage-1)*pageParam.pageRows)+','+str(pageParam.pageRows),queryParams).fetchall()
        pageParam.totalRecords=BllApproveInfo().execute(SQL.replace('*','count(*)',1),queryParams).fetchone()[0]
        info_list = Utils.mysqlTable2Model(info_list)
        data = info_list
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})

# 获取待我审批的审批信息列表Json数据
@require_http_methods(['GET'])
def getMyReceiveApproveInfoListJson(request):
    if request.method == 'GET':
        ApproveInfoCode = request.GET.get('ApproveInfoCode', '')
        CreateUserName = request.GET.get('CreateUserName', '')
        ApproveTypeCode = request.GET.get('ApproveTypeCode', '')
        CurrentUserApproveStatus = request.GET.get('CurrentUserApproveStatus', '')
        curPage = int(request.GET.get('page', '1'))
        pageSize = int(request.GET.get('limit', '10'))
        pageParam = PageParam(curPage,pageSize)
        user_ = request.session['login_user']
        SQL="""
        SELECT * FROM( SELECT a.*,GROUP_CONCAT(CONCAT(c.RealName,'(',c.UserCode,')')  ORDER BY b.SortIndex ASC separator '=>') AS ApproveInfoProcess,
        SUM(CASE WHEN b.ApproveUserId='"""+user_['UserId']+"""' THEN b.ApproveStatus END) AS CurrentUserApproveStatus FROM rms_approveinfo a 
        LEFT JOIN rms_approveinfoprocess b ON a.ApproveInfoId=b.ApproveInfoId LEFT JOIN rms_user c ON b.ApproveUserId=c.UserId  GROUP BY a.ApproveInfoId 
        HAVING GROUP_CONCAT(c.UserId) LIKE '%"""+user_['UserId']+"""%' ORDER BY a.CreateDate DESC  ) nt WHERE CurrentUserApproveStatus>1
        """
        if(ApproveInfoCode):
            SQL+= " and ApproveInfoCode like '%"+ApproveInfoCode+"%'"
        if(CreateUserName):
            SQL+= " and CreateUserName like '%"+CreateUserName+"%'"
        if(ApproveTypeCode):
            SQL+=" and ApproveTypeCode = '"+ApproveTypeCode+"'"
        if(CurrentUserApproveStatus):
            SQL+=" and CurrentUserApproveStatus = "+CurrentUserApproveStatus
        queryParams={}
        info_list=BllApproveInfo().execute(SQL+ ' limit '+ str((pageParam.curPage-1)*pageParam.pageRows)+','+str(pageParam.pageRows),queryParams).fetchall()
        pageParam.totalRecords=BllApproveInfo().execute(SQL.replace('*','count(*)',1),queryParams).fetchone()[0]
        info_list = Utils.mysqlTable2Model(info_list)
        data = info_list
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})


# 保存审批类型数据
@require_http_methods(['POST'])
@csrf_exempt
def saveApproveTypeData(request):
    try:
        if request.method == 'POST':
            ApproveTypeId = request.POST.get('ApproveTypeId')
            ApproveTypeCode = request.POST.get('ApproveTypeCode','')
            ApproveTypeName = request.POST.get('ApproveTypeName','')
            Description = request.POST.get('Description')
            approveTypeProcessValue = request.POST.get('approveTypeProcess')
            
            # 根据RoleId是否有值判断是创建还是修改
            if not ApproveTypeId:
                
                approveType = BllApproveType().findEntity(or_(EntityApproveType.ApproveTypeCode == ApproveTypeCode,EntityApproveType.ApproveTypeName==ApproveTypeName))
                if approveType is None:
                    ApproveTypeId = str(Utils.UUID())
                    SQL = """SELECT max(SortIndex) as SortIndex FROM `rms_approvetype`;"""
                    role_max_obj = BllApproveType().execute(SQL).fetchone()
                    approveType = EntityApproveType(ApproveTypeId=ApproveTypeId, ApproveTypeCode=ApproveTypeCode, ApproveTypeName=ApproveTypeName,Description=Description,
                                    SortIndex=int(role_max_obj.SortIndex or '0')+1,CreateDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    BllApproveType().insert(approveType)
                else:
                    return JsonResponse(Utils.resultData('0', '类型代码或名称已存在', ''))
            else:
                approveType = BllApproveType().findEntity(ApproveTypeId)
                approveType_ = BllApproveType().findEntity(or_(EntityApproveType.ApproveTypeCode == ApproveTypeCode,EntityApproveType.ApproveTypeName==ApproveTypeName))
                if approveType_ is None or approveType.ApproveTypeId==approveType_.ApproveTypeId:
                    approveType.ApproveTypeId = ApproveTypeId
                    approveType.ApproveTypeName = ApproveTypeName
                    approveType.ApproveTypeCode = ApproveTypeCode
                    approveType.Description = Description
                    BllApproveType().update(approveType)
                else:
                    return JsonResponse(Utils.resultData('0', '类型代码或名称已存在', ''))
            # 将存入的字符串格式以逗号分隔转换成列表
            BllApproveTypeProcess().delete(EntityApproveTypeProcess.ApproveTypeId == ApproveTypeId)
            if approveTypeProcessValue:
                approveTypeProcessList = approveTypeProcessValue.split(',')
                for index, approveTypeProcess in enumerate(approveTypeProcessList):
                    userEntity=BllUser().findEntity(approveTypeProcess)
                    entity_module = EntityApproveTypeProcess(Id=str(Utils.UUID()),ApproveTypeId=ApproveTypeId, ObjectType=1, ObjectId=approveTypeProcess,ObjectName='{0}({1})'.format(userEntity.RealName,userEntity.UserCode), SortIndex=index+1,CreateDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    BllApproveTypeProcess().insert(entity_module)
            return JsonResponse(Utils.resultData('1', ' 保存成功'))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))

# 提交审批决定
@require_http_methods(['POST'])
@csrf_exempt
def summitApproveDecide(request):
    # try:
        if request.method == 'POST':
            ApproveInfoId = request.POST.get('ApproveInfoId')
            ApproveDecide = request.POST.get('ApproveDecide')
            Description = request.POST.get('Description')
            user_ = request.session['login_user']
            print('dsssssssssssssssssssss',ApproveInfoId)
            BllApproveInfo().submitApprovalAndNextStep(ApproveInfoId,(True if ApproveDecide=='1' else False),Description,user_["UserId"])
            return JsonResponse(Utils.resultData('1', ' 执行成功'))
    # except Exception as e:
    #     return JsonResponse(Utils.resultData('0', str(e), ''))



# 删除审批类型
@require_http_methods(['POST'])
@csrf_exempt
def deleteApproveType(request):
    try:
        if request.method == 'POST':
            deleteIds = request.POST.get("deleteIds",'')
            deleteIds=deleteIds.split(',')
            for deleteId in deleteIds:
                BllApproveTypeProcess().delete(EntityApproveTypeProcess.ApproveTypeId == deleteId)
                BllApproveType().delete(EntityApproveType.ApproveTypeId==deleteId)
            return JsonResponse(Utils.resultData('1', '删除成功', ''))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))