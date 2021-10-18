from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import json
import base64
import pdfkit
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote

from Business.BllApproveInfo import *
from Business.BllApproveInfoProcess import *
from Business.BllPurchaseOrder import *
from Business.BllPurchaseOrderDetailed import *
from Business.BllAcceptanceOrder import *
from Business.BllAcceptanceOrderDetailed import *
from Business.BllMedicamentTemplate import *
from Business.BllMedicament import *
from Business.BllPeriodCheck import *
from Business.BllPeriodCheckDetailed import *
from DataEntity.EntityPurchaseOrder import *
from DataEntity.EntityPurchaseOrderDetailed import *
from DataEntity.EntityAcceptanceOrder import *
from DataEntity.EntityAcceptanceOrderDetailed import *
from DataEntity.EntityMedicamentTemplate import *
from DataEntity.EntityPeriodCheck import *
from DataEntity.EntityPeriodCheckDetailed import *
from DataEntity.EntityMedicament import *
from Lib.searchDrug import GetDrugTypeData
from Lib.Utils import *
from Lib.reportExcel import *
from Lib.Model import *

@require_http_methods(['GET'])
def purchaseIndex(request):
    if request.method == 'GET':
        return render(request, 'standard/purchaseIndex.html', locals())

@require_http_methods(['GET'])
def purchaseWaitingIndex(request):
    if request.method == 'GET':
        return render(request, 'standard/purchaseWaitingIndex.html', locals())

@require_http_methods(['GET'])
def purchaseCompleteIndex(request):
    if request.method == 'GET':
        return render(request, 'standard/purchaseCompleteIndex.html', locals())

@require_http_methods(['GET'])
def acceptanceIndex(request):
    if request.method == 'GET':
        return render(request, 'standard/acceptanceIndex.html', locals())

@require_http_methods(['GET'])
def periodCheckIndex(request):
    if request.method == 'GET':
        return render(request, 'standard/periodCheckIndex.html', locals())

@require_http_methods(['GET'])
def periodCheckDrugIndex(request):
    if request.method == 'GET':
        VarietyId= request.GET.get('VarietyId','')
        return render(request, 'standard/periodCheckDrugIndex.html', locals())

@require_http_methods(['GET'])
def periodCheckDrugAnonIndex(request):
    if request.method == 'GET':
        return render(request, 'standard/periodCheckDrugAnonIndex.html', locals())

def periodCheckDrugFailureIndex(request):
    if request.method == 'GET':
        VarietyId= request.GET.get('VarietyId','')
        return render(request, 'standard/periodCheckDrugFailureIndex.html', locals())

@require_http_methods(['GET'])
def purchaseForm(request):
    if request.method == 'GET':
        PurchaseOrderId= request.GET.get('PurchaseOrderId','')
        model=BllPurchaseOrder().findEntity(PurchaseOrderId)
        PurchaseOrderContent='[]'
        if(model is not None):
            PurchaseOrderContent=model.PurchaseOrderContent
            try:
                PurchaseOrderContent=json.loads(PurchaseOrderContent)
            except:
                PurchaseOrderContent=[]
        NewPurchaseOrderCode='10'+Utils.createOrderCode()
        return render(request, 'standard/purchaseForm.html', locals())

@require_http_methods(['GET'])
def purchaseDrugForm(request):
    if request.method == 'GET':
        return render(request, 'standard/purchaseDrugForm.html', locals())

@require_http_methods(['GET'])
def acceptanceDrugForm(request):
    if request.method == 'GET':
        acceptanceDrugData= request.GET.get("acceptanceDrugData",'')
        if(acceptanceDrugData==''):
            model=None
        else:
            model=json.loads(acceptanceDrugData)
        return render(request, 'standard/acceptanceDrugForm.html', locals())

@require_http_methods(['GET'])
def acceptanceForm(request):
    if request.method == 'GET':
        AcceptanceOrderId= request.GET.get('AcceptanceOrderId','')
        model=BllAcceptanceOrder().findEntity(AcceptanceOrderId)
        AcceptanceOrderContent='[]'
        if(model is not None):
            AcceptanceOrderContent=model.AcceptanceOrderContent
            try:
                AcceptanceOrderContent=json.loads(AcceptanceOrderContent)
            except:
                AcceptanceOrderContent=[]
        NewAcceptanceOrderCode='20'+Utils.createOrderCode()
        return render(request, 'standard/acceptanceForm.html', locals())

@require_http_methods(['GET'])
def acceptanceView(request):
    if request.method == 'GET':
        AcceptanceOrderId= request.GET.get('AcceptanceOrderId','')
        model=BllAcceptanceOrder().findEntity(AcceptanceOrderId)
        AcceptanceOrderContent='[]'
        if(model is not None):
            AcceptanceOrderContent=model.AcceptanceOrderContent
            try:
                AcceptanceOrderContent=json.loads(AcceptanceOrderContent)
            except:
                AcceptanceOrderContent=[]
        NewAcceptanceOrderCode='20'+Utils.createOrderCode()
        return render(request, 'standard/acceptanceView.html', locals())
        

@require_http_methods(['GET'])
def periodCheckForm(request):
    if request.method == 'GET':
        PeriodCheckId= request.GET.get('PeriodCheckId','')
        model=BllPeriodCheck().findEntity(PeriodCheckId)
        return render(request, 'standard/periodCheckForm.html', locals())

@require_http_methods(['GET'])
def periodCheckDrugForm(request):
    if request.method == 'GET':
        PeriodCheckDetailedId= request.GET.get('PeriodCheckDetailedId','')
        PeriodCheckId= request.GET.get('PeriodCheckId','')
        DrugCode= request.GET.get('DrugCode','')
        drugModel=BllMedicament().findEntity(EntityMedicament.BarCode==DrugCode)
        model=BllPeriodCheckDetailed().findEntity(and_(EntityPeriodCheckDetailed.PeriodCheckId==PeriodCheckId,
                                            EntityPeriodCheckDetailed.DrugId==drugModel.MedicamentId))
        return render(request, 'standard/periodCheckDrugForm.html', locals())

@require_http_methods(['GET'])
def purchaseView(request):
    if request.method == 'GET':
        PurchaseOrderId= request.GET.get('PurchaseOrderId','')
        model=BllPurchaseOrder().findEntity(PurchaseOrderId)
        PurchaseOrderContent='[]'
        if(model is not None):
            PurchaseOrderContent=model.PurchaseOrderContent
            try:
                PurchaseOrderContent=json.loads(PurchaseOrderContent)
            except:
                PurchaseOrderContent=[]
        NewPurchaseOrderCode='10'+Utils.createOrderCode()
        return render(request, 'standard/purchaseView.html', locals())

@require_http_methods(['GET'])
def photographForm(request):
    if request.method == 'GET':
        return render(request, 'standard/photographForm.html', locals())

@require_http_methods(['GET'])
def cropperImgForm(request):
    if request.method == 'GET':
        return render(request, 'standard/cropperImgForm.html', locals())

@require_http_methods(['GET'])
def acceptancePDFView(request):
    if request.method == 'GET':
        AcceptanceOrderId= request.GET.get("AcceptanceOrderId",'')
        acceptanceDrugListData= request.GET.get("acceptanceDrugListData",'')
        AcceptanceOrderModel=BllAcceptanceOrder().findEntity(AcceptanceOrderId)
        AcceptanceOrderCode= AcceptanceOrderModel.AcceptanceOrderCode
        AcceptanceOrderModel=Utils.resultAlchemyData(AcceptanceOrderModel)
        AcceptanceOrderModel=json.loads(AcceptanceOrderModel)

        AcceptanceUser=BllUser().findEntity(AcceptanceOrderModel['AcceptanceUserId'])
        signUrl=''
        if(int(AcceptanceOrderModel['AcceptanceOrderStatus'])==2):
            if(os.path.exists(os.getcwd()+AcceptanceUser.SignUrl)):
                with open(os.getcwd()+AcceptanceUser.SignUrl, 'rb') as f:
                    base64_data = base64.b64encode(f.read())
                    s = base64_data.decode()
                    signUrl='data:image/png;base64,%s'%s
                AcceptanceOrderModel.update(SignUrl=signUrl)
        else:
            AcceptanceOrderModel['AcceptanceDate']=''
        if(acceptanceDrugListData==''):
            modelList=[]
        else:
            modelList=json.loads(acceptanceDrugListData)
        return render(request, 'standard/acceptancePDFView.html', locals())

@require_http_methods(['GET'])
def purchasePDFView(request):
    if request.method == 'GET':
        PurchaseOrderId= request.GET.get("PurchaseOrderId",'')
        purchaseOrderModel=BllPurchaseOrder().findEntity(PurchaseOrderId)
        PurchaseOrderCode=purchaseOrderModel.PurchaseOrderCode
        PurchaseOrderContent='[]'
        if(purchaseOrderModel is not None):
            PurchaseOrderContent=purchaseOrderModel.PurchaseOrderContent
            try:
                PurchaseOrderContent=json.loads(PurchaseOrderContent)
            except:
                PurchaseOrderContent=[]
        purchaseOrderModel=Utils.resultAlchemyData(purchaseOrderModel)
        purchaseOrderModel=json.loads(purchaseOrderModel)
        purchaseOrderModel['table']=PurchaseOrderContent
        SQL="""
            SELECT a.ApproveDate,b.SignUrl FROM rms_approveinfoprocess a LEFT JOIN rms_user b ON a.ApproveUserId=b.UserId 
            WHERE a.ApproveInfoId='"""+purchaseOrderModel['ApproveInfoId']+"""'  ORDER BY a.SortIndex ASC
        """
        approveProcessList = BllApproveInfoProcess().execute(SQL).fetchall()
        approveProcessList = Utils.mysqlTable2Model(approveProcessList)
        approveCount=len(approveProcessList)
        for index, approveProcess in enumerate(approveProcessList):
            purchaseOrderModel['ApproveDate'+str(index+1)]=approveProcess['ApproveDate']
            if(not approveProcess['SignUrl']):
                continue
            signUrlPath=os.getcwd()+approveProcess['SignUrl']
            
            if(os.path.exists(signUrlPath)):
                signUrl=''
                with open(signUrlPath, 'rb') as f:
                    base64_data = base64.b64encode(f.read())
                    s = base64_data.decode()
                    signUrl='data:image/png;base64,%s'%s
                purchaseOrderModel['SignUrl'+str(index+1)]=signUrl

        return render(request, 'standard/purchasePDFView.html', locals())

@require_http_methods(['GET'])
def periodCheckView(request):
    if request.method == 'GET':
        PeriodCheckId= request.GET.get('PeriodCheckId','')
        model=BllPeriodCheck().findEntity(PeriodCheckId)
        return render(request, 'standard/periodCheckView.html', locals())

@require_http_methods(['GET'])
def periodCheckDrugDetailedInfo(request):
    if request.method == 'GET':
        DrugId= request.GET.get('DrugId','')
        drugModel=BllMedicament().findEntity(DrugId)
        drugPeriodCheckDetailedList=BllPeriodCheckDetailed().getPeriodCheckDetailedListByDrugId(DrugId)
        checkCount=len(drugPeriodCheckDetailedList)+1
        return render(request, 'standard/periodCheckDrugDetailedInfo.html', locals())

# 输入试剂名称自动搜索试剂列表处理函数
@require_http_methods(['GET'])
def autoSearchDrugList(request):
    if request.method == 'GET':
        time1 = time.time()
        CASNumber = request.GET.get('CASNumber', '')
        if not CASNumber:
            search_word = request.GET.get('keyWord')
            data_list = GetDrugTypeData.search_data(search_word)
            time2 = time.time()
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data_list)),'code' : 0,'msg':''})
        else:
            logger.info('CASNumber被传入值')
            return JsonResponse({'data': '','code' : 1,'msg':''})

# 获取采购单数据列表
@require_http_methods(['GET'])
def getPurchaseOrderListJson(request):
    if request.method == 'GET':
        PurchaseOrderCode = request.GET.get('PurchaseOrderCode', '')
        CreateUserName = request.GET.get('CreateUserName', '')
        PurchaseOrderDrugInfo = request.GET.get('PurchaseOrderDrugInfo', '')
        PurchaseOrderStatus = request.GET.get('PurchaseOrderStatus', '')
        curPage = int(request.GET.get('page', '1'))
        pageSize = int(request.GET.get('limit', '10'))
        pageParam = PageParam(curPage,pageSize)
        data = BllPurchaseOrder().getPurchaseOrderList(pageParam,PurchaseOrderCode,CreateUserName,PurchaseOrderDrugInfo,PurchaseOrderStatus)
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})

# 获取等待采购数据列表
@require_http_methods(['GET'])
def getWaitingPurchaseListJson(request):
    if request.method == 'GET':
        PurchaseOrderCode = request.GET.get('PurchaseOrderCode', '')
        CreateUserName = request.GET.get('CreateUserName', '')
        PurchaseOrderDrugInfo = request.GET.get('PurchaseOrderDrugInfo', '')
        curPage = int(request.GET.get('page', '1'))
        pageSize = int(request.GET.get('limit', '10'))
        pageParam = PageParam(curPage,pageSize)
        data = BllPurchaseOrder().getWaitingPurchaseList(pageParam,PurchaseOrderCode,CreateUserName,PurchaseOrderDrugInfo)
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})

# 获取完成采购数据列表
@require_http_methods(['GET'])
def getCompletePurchaseListJson(request):
    if request.method == 'GET':
        PurchaseOrderCode = request.GET.get('PurchaseOrderCode', '')
        CreateUserName = request.GET.get('CreateUserName', '')
        PurchaseOrderDrugInfo = request.GET.get('PurchaseOrderDrugInfo', '')
        curPage = int(request.GET.get('page', '1'))
        pageSize = int(request.GET.get('limit', '10'))
        pageParam = PageParam(curPage,pageSize)
        data = BllPurchaseOrder().getCompletePurchaseList(pageParam,PurchaseOrderCode,CreateUserName,PurchaseOrderDrugInfo)
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})

# 获取验收单数据列表
@require_http_methods(['GET'])
def getAcceptanceOrderListJson(request):
    if request.method == 'GET':
        AcceptanceOrderCode = request.GET.get('AcceptanceOrderCode', '')
        CreateUserName = request.GET.get('CreateUserName', '')
        AcceptanceOrderDrugInfo = request.GET.get('AcceptanceOrderDrugInfo', '')
        AcceptanceOrderStatus = request.GET.get('AcceptanceOrderStatus', '')
        curPage = int(request.GET.get('page', '1'))
        pageSize = int(request.GET.get('limit', '10'))
        pageParam = PageParam(curPage,pageSize)
        data = BllAcceptanceOrder().getAcceptanceOrderList(pageParam,AcceptanceOrderCode,CreateUserName,AcceptanceOrderDrugInfo,AcceptanceOrderStatus)
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})

# 获取期间核查数据列表
@require_http_methods(['GET'])
def getPeriodCheckListJson(request):
    if request.method == 'GET':
        PeriodCheckCode = request.GET.get('PeriodCheckCode', '')
        CreateUserName = request.GET.get('CreateUserName', '')
        PeriodCheckStatus = request.GET.get('PeriodCheckStatus', '')
        curPage = int(request.GET.get('page', '1'))
        pageSize = int(request.GET.get('limit', '10'))
        pageParam = PageParam(curPage,pageSize)
        data = BllPeriodCheck().getPeriodCheckList(pageParam,PeriodCheckCode,CreateUserName,PeriodCheckStatus)
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})

# # 获取期间核查详细数据列表
# @require_http_methods(['GET'])
# def getPeriodCheckDetailedListJson(request):
#     if request.method == 'GET':
#         PeriodCheckId = request.GET.get('PeriodCheckId', '')
#         curPage = int(request.GET.get('page', '1'))
#         pageSize = int(request.GET.get('limit', '10'))
#         pageParam = PageParam(curPage,pageSize)
#         user_ = request.session['login_user']
#         SQL="""
#             SELECT * FROM(SELECT a.*,b.Name,b.BarCode,b.CASNumber,CONCAT(b.Speci,b.SpeciUnit) AS Speci 
#             FROM rms_periodcheckdetailed a LEFT JOIN rms_medicament b ON a.DrugId=b.MedicamentId) nt
#             WHERE PeriodCheckId='"""+PeriodCheckId+"""'
#         """
#         queryParams={}
#         info_list=BllPeriodCheckDetailed().execute(SQL+ ' limit '+ str((pageParam.curPage-1)*pageParam.pageRows)+','+str(pageParam.pageRows),queryParams).fetchall()
#         pageParam.totalRecords=BllPeriodCheckDetailed().execute(SQL.replace('*','count(*)',1),queryParams).fetchone()[0]
#         info_list = Utils.mysqlTable2Model(info_list)
#         data = info_list
#         return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})

# 获取期间核查详细数据列表
@require_http_methods(['GET'])
def getPeriodCheckDetailedListJson(request):
    if request.method == 'GET':
        VarietyId = request.GET.get('VarietyId', '')
        curPage = int(request.GET.get('page', '1'))
        pageSize = int(request.GET.get('limit', '10'))
        pageParam = PageParam(curPage,pageSize)
        user_ = request.session['login_user']
        # SQL="""
        #     SELECT * FROM(SELECT a.*,b.Name,b.BarCode,b.CASNumber,CONCAT(b.Speci,b.SpeciUnit) AS Speci 
        #     FROM rms_periodcheckdetailed a LEFT JOIN rms_medicament b ON a.DrugId=b.MedicamentId) nt
        #     WHERE PeriodCheckId='"""+PeriodCheckId+"""'
        # """
        SQL="""
            SELECT * FROM (SELECT MedicamentId,Place,VarietyId,LastPeriodCheckStatus,Name,BarCode,CASNumber,CONCAT(Speci,SpeciUnit) AS Speci, 
            (CASE WHEN LastPeriodCheckDate THEN LastPeriodCheckDate ELSE PutInDate  END) 
            AS LastPeriodCheckDate  FROM rms_medicament) a LEFT JOIN rms_medicamentvariety b 
            ON a.VarietyId=b.VarietyId 
            WHERE TO_DAYS(date_add(a.LastPeriodCheckDate, interval b.PeriodCheckIntervalValue day)) <= TO_DAYS(NOW())
        """
        if(VarietyId):
            SQL+=' AND a.VarietyId='+"'"+ VarietyId+"'"

        queryParams={}
        info_list=BllPeriodCheckDetailed().execute(SQL+ ' limit '+ str((pageParam.curPage-1)*pageParam.pageRows)+','+str(pageParam.pageRows),queryParams).fetchall()
        pageParam.totalRecords=BllPeriodCheckDetailed().execute(SQL.replace('*','count(*)',1),queryParams).fetchone()[0]
        info_list = Utils.mysqlTable2Model(info_list)
        data = info_list
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})

# 获取期间核查不合格数据列表
@require_http_methods(['GET'])
def getPeriodCheckFailureListJson(request):
    if request.method == 'GET':
        VarietyId = request.GET.get('VarietyId', '')
        Name = request.GET.get('Name', '')
        BarCode = request.GET.get('BarCode', '')
        curPage = int(request.GET.get('page', '1'))
        pageSize = int(request.GET.get('limit', '10'))
        pageParam = PageParam(curPage,pageSize)
        user_ = request.session['login_user']
        # SQL="""
        #     SELECT * FROM(SELECT a.*,b.Name,b.BarCode,b.CASNumber,CONCAT(b.Speci,b.SpeciUnit) AS Speci 
        #     FROM rms_periodcheckdetailed a LEFT JOIN rms_medicament b ON a.DrugId=b.MedicamentId) nt
        #     WHERE PeriodCheckId='"""+PeriodCheckId+"""'
        # """
        SQL="""
            SELECT * FROM(
            SELECT  a.*,b.`Name`,b.BarCode,b.CASNumber,CONCAT(b.Speci,b.SpeciUnit)AS Speci 
            FROM rms_periodcheckdetailed a LEFT JOIN rms_medicament b ON a.DrugId=b.MedicamentId 
            WHERE a.`Status`=1 ORDER BY CreateDate DESC) nt WHERE 1=1
        """
        if(Name):
            SQL+=" AND Name like '%"+Name+"%'"
        if(BarCode):
            SQL+=" AND BarCode like '%"+BarCode+"%'"
        queryParams={}
        info_list=BllPeriodCheckDetailed().execute(SQL+ ' limit '+ str((pageParam.curPage-1)*pageParam.pageRows)+','+str(pageParam.pageRows),queryParams).fetchall()
        pageParam.totalRecords=BllPeriodCheckDetailed().execute(SQL.replace('*','count(*)',1),queryParams).fetchone()[0]
        info_list = Utils.mysqlTable2Model(info_list)
        data = info_list
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})


# 保存采购数据
@require_http_methods(['POST'])
@csrf_exempt
def savePurchaseOrderData(request):
    try:
        if request.method == 'POST':
            PurchaseOrderId = request.POST['PurchaseOrderId']
            PurchaseOrderCode = request.POST['PurchaseOrderCode']
            PurchaseOrderContent = request.POST['PurchaseOrderContent']
            PurchaseOrderDrugInfo = request.POST['PurchaseOrderDrugInfo']
            Description = request.POST['Description']
            PurchaseOrderStatus = request.POST.get("PurchaseOrderStatus",1)
            PurchaseOrderTotalCount = request.POST.get("PurchaseOrderTotalCount",0)
            ApproveInfoContent = request.POST.get("ApproveInfoContent",'')

            user_ = request.session['login_user']
            if not PurchaseOrderId:
                
                entity = BllPurchaseOrder().findEntity(EntityPurchaseOrder.PurchaseOrderCode == PurchaseOrderCode)
                if entity is None:
                    PurchaseOrderId = str(Utils.UUID())
                    entity = EntityPurchaseOrder(PurchaseOrderId=PurchaseOrderId, PurchaseOrderCode=PurchaseOrderCode, ApproveInfoId='',IsCompletePurchase=0,
                                        PurchaseOrderContent=PurchaseOrderContent, Description=Description, PurchaseOrderStatus=PurchaseOrderStatus,
                                        CreateDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),CreateUserId = user_['UserId'], 
                                        CreateUserName ='{0}({1})'.format(user_['RealName'],user_['UserCode']),PurchaseOrderTotalCount=PurchaseOrderTotalCount,PurchaseOrderDrugInfo=PurchaseOrderDrugInfo)
                    BllPurchaseOrder().insert(entity)
                else:
                    return JsonResponse(Utils.resultData('0', '单号必须唯一, 该单号已存在', ''))
            else:
                entity = BllPurchaseOrder().findEntity(PurchaseOrderId)
                entity_ = BllPurchaseOrder().findEntity(EntityPurchaseOrder.PurchaseOrderCode == PurchaseOrderCode)

                if entity_ is None or entity.PurchaseOrderId == entity_.PurchaseOrderId:
                    entity.PurchaseOrderId = PurchaseOrderId
                    entity.PurchaseOrderCode = PurchaseOrderCode
                    entity.PurchaseOrderContent = PurchaseOrderContent
                    entity.PurchaseOrderDrugInfo = PurchaseOrderDrugInfo
                    entity.PurchaseOrderTotalCount = PurchaseOrderTotalCount
                    entity.Description = Description
                    entity.PurchaseOrderStatus = PurchaseOrderStatus
                    BllPurchaseOrder().update(entity)
                else:
                    return JsonResponse(Utils.resultData('0', '单号必须唯一, 该单号已存在', ''))
            if(int(PurchaseOrderStatus)==2):
               approveInfoId= BllApproveInfo().addApproveInfo(ApproveTypeAllCode.Purchase,ApproveInfoContent,PurchaseOrderId,PurchaseOrderCode,Description,user_['UserId'])
               entity.ApproveInfoId=approveInfoId
               BllPurchaseOrder().update(entity)
            return JsonResponse(Utils.resultData('1', '保存成功', ''))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))

# 设置完采购
@require_http_methods(['POST'])
@csrf_exempt
def setCompletePurchase(request):
    try:
        if request.method == 'POST':
            user_ = request.session['login_user']
            PurchaseOrderId = request.POST.get("PurchaseOrderId",'')
            entity= BllPurchaseOrder().findEntity(PurchaseOrderId)
            entity.IsCompletePurchase=1
            entity.PurchaseDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            entity.PurchaseUserId=user_['UserId']
            entity.PurchaseUserName='{0}({1})'.format(user_['RealName'],user_['UserCode'])
            BllPurchaseOrder().update(entity)
            AcceptanceOrderId = str(Utils.UUID())
            NewAcceptanceOrderCode='20'+Utils.createOrderCode()
            entity = EntityAcceptanceOrder(AcceptanceOrderId=AcceptanceOrderId, AcceptanceOrderCode=NewAcceptanceOrderCode, AcceptanceOrderContent=entity.PurchaseOrderContent,
                                AcceptanceOrderDrugInfo=entity.PurchaseOrderDrugInfo, Description='', AcceptanceOrderStatus=1,
                                CreateDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),CreateUserId = user_['UserId'], 
                                CreateUserName ='{0}({1})'.format(user_['RealName'],user_['UserCode']),AcceptanceOrderTotalCount=entity.PurchaseOrderTotalCount)
            BllAcceptanceOrder().insert(entity)
            return JsonResponse(Utils.resultData('1', '设置成功', ''))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))


# 删除采购单
@require_http_methods(['POST'])
@csrf_exempt
def deletePurchaseOrder(request):
    try:
        if request.method == 'POST':
            deleteIds = request.POST.get("deleteIds",'')
            deleteIds=deleteIds.split(',')
            for deleteId in deleteIds:
                BllPurchaseOrder().delete(EntityPurchaseOrder.PurchaseOrderId==deleteId)
            return JsonResponse(Utils.resultData('1', '删除成功', ''))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))

# 保存拍照信息
@require_http_methods(['POST'])
@csrf_exempt
def savePhotographData(request):
    try:
        if request.method == 'POST':
            pictureBase64 = request.POST.get("pictureBase64",'')

            returnPath='UploadResources/Pictures/'+datetime.datetime.now().strftime('%Y%m%d')
            createPath=os.getcwd()+'/static/'+returnPath
            Utils.mkdir(createPath)
            imgdata = base64.b64decode(pictureBase64)
            fileName=Utils.getFileName()+'.png'
            file = open(createPath+'/'+fileName,'wb')
            file.write(imgdata)
            file.close()
            return JsonResponse(Utils.resultData('1', '保存成功', returnPath+'/'+fileName))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))

# 保存验收单数据
@require_http_methods(['POST'])
@csrf_exempt
def saveAcceptanceOrderData(request):
    try:
        if request.method == 'POST':
            AcceptanceOrderId = request.POST['AcceptanceOrderId']
            AcceptanceOrderCode = request.POST['AcceptanceOrderCode']
            AcceptanceOrderContent = request.POST['AcceptanceOrderContent']
            AcceptanceOrderDrugInfo = request.POST['AcceptanceOrderDrugInfo']
            AcceptanceOrderImageUrl = request.POST.get('AcceptanceOrderImageUrl');
            Description = request.POST['Description']
            AcceptanceOrderStatus = request.POST.get("AcceptanceOrderStatus",1)
            AcceptanceOrderTotalCount = request.POST.get("AcceptanceOrderTotalCount",0)

            user_ = request.session['login_user']
            if not AcceptanceOrderId:
                entity = BllAcceptanceOrder().findEntity(EntityAcceptanceOrder.AcceptanceOrderCode == AcceptanceOrderCode)
                if entity is None:
                    AcceptanceOrderId = str(Utils.UUID())
                    entity = EntityAcceptanceOrder(AcceptanceOrderId=AcceptanceOrderId,AcceptanceOrderCode=AcceptanceOrderCode,
                                        AcceptanceOrderContent=AcceptanceOrderContent, Description=Description, AcceptanceOrderStatus=AcceptanceOrderStatus,
                                        CreateDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),CreateUserId = user_['UserId'], 
                                        CreateUserName ='{0}({1})'.format(user_['RealName'],user_['UserCode']),
                                        AcceptanceDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),AcceptanceUserId = user_['UserId'], 
                                        AcceptanceUserName ='{0}({1})'.format(user_['RealName'],user_['UserCode']),
                                        AcceptanceOrderTotalCount=AcceptanceOrderTotalCount,AcceptanceOrderDrugInfo=AcceptanceOrderDrugInfo,
                                        AcceptanceOrderImageUrl=AcceptanceOrderImageUrl)
                    BllAcceptanceOrder().insert(entity)
                else:
                    return JsonResponse(Utils.resultData('0', '单号必须唯一, 该单号已存在', ''))
            else:
                entity = BllAcceptanceOrder().findEntity(AcceptanceOrderId)
                entity_ = BllAcceptanceOrder().findEntity(EntityAcceptanceOrder.AcceptanceOrderId == AcceptanceOrderId)
                
                if entity_ is None or entity.AcceptanceOrderId == entity_.AcceptanceOrderId:
                    if(int(AcceptanceOrderStatus)==2):
                        entity.AcceptanceDate= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        entity.AcceptanceUserId=user_['UserId']
                        entity.AcceptanceUserName='{0}({1})'.format(user_['RealName'],user_['UserCode'])
                    entity.AcceptanceOrderId = AcceptanceOrderId
                    entity.AcceptanceOrderCode = AcceptanceOrderCode
                    entity.AcceptanceOrderContent = AcceptanceOrderContent
                    entity.AcceptanceOrderDrugInfo = AcceptanceOrderDrugInfo
                    entity.AcceptanceOrderTotalCount = AcceptanceOrderTotalCount
                    entity.AcceptanceOrderImageUrl = AcceptanceOrderImageUrl
                    entity.Description = Description
                    entity.AcceptanceOrderStatus = AcceptanceOrderStatus
                    BllAcceptanceOrder().update(entity)
                else:
                    return JsonResponse(Utils.resultData('0', '单号必须唯一, 该单号已存在', ''))

            if(int(AcceptanceOrderStatus)==2):
                # 随机生成uuid字符串作为主键
                str_uuid = str(Utils.UUID())
                # 获取当前系统时间
                CreateDate = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                # 获取创建用户姓名
                CreateUserName = request.session['login_user']['RealName']
                CreateUserId = request.session['login_user']['UserId']
                CustomerId = request.session['login_user']['CustomerId']
                SQL = """
                SELECT  BarCodeCount, StartBarCode FROM `RMS_MedicamentTemplate` where StartBarCode =  (SELECT MAX(StartBarCode) from RMS_MedicamentTemplate)
                """
                tem_obj = BllMedicament().execute(SQL).fetchone()
                if tem_obj is None:
                    max_barcode = 100001
                else:
                    max_barcode = tem_obj.StartBarCode
                    BarCodeCount = tem_obj.BarCodeCount
                    # 获取最大的开始barcode + 数量
                    max_barcode = int(max_barcode) + int(BarCodeCount)
                StartBarCode = max_barcode
                AcceptanceOrderContentList= json.loads(AcceptanceOrderContent)
                newPutInContent=[]
                for model in AcceptanceOrderContentList:
                    newModel=model
                    newModel['Name']=model.get('DrugName','')
                    newModel['ExportCount']=int(model.get('DrugCount','1'))
                    newPutInContent.insert(0,newModel)
                AcceptanceOrderContent=json.dumps(newPutInContent)
                # 新增试剂模板记录
                templateEntity = EntityMedicamentTemplate(TemplateId=str_uuid, TemplateName='40'+Utils.createOrderCode(), ClientId='',
                                                ClientName='', TemplateContent=AcceptanceOrderContent,
                                                CreateDate=CreateDate,  CreateUserId=CreateUserId, CustomerId=CustomerId,
                                                CreateUserName=CreateUserName, IsWaitExport=1, BarCodeCount=int(AcceptanceOrderTotalCount),
                                                StartBarCode=str(StartBarCode))
                BllMedicamentTemplate().insert(templateEntity)
            return JsonResponse(Utils.resultData('1', '保存成功', ''))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))

# 保存期间核查数据
@require_http_methods(['POST'])
@csrf_exempt
def savePeriodCheckData(request):
    try:
        if request.method == 'POST':
            PeriodCheckId = request.POST.get('PeriodCheckId','')
            Description = request.POST.get('Description','')
            PeriodCheckStatus = int(request.POST.get('PeriodCheckStatus','0'))

            user_ = request.session['login_user']
            if not PeriodCheckId:
                noCompleteCount= BllPeriodCheck().findCount(EntityPeriodCheck.PeriodCheckStatus==1)
                if(noCompleteCount!=0):
                    return JsonResponse(Utils.resultData('0', '有未结束的核查进行中！', ''))
                PeriodCheckId = str(Utils.UUID())
                currentNormalCount = BllMedicament().findCount(EntityMedicament.Status==1)
                SQL = """SELECT max(SortIndex) as SortIndex FROM `rms_periodcheck`;"""
                maxSortIndexRow = BllMedicament().execute(SQL).fetchone()
                entity = EntityPeriodCheck(PeriodCheckId=PeriodCheckId,PeriodCheckCode='30'+Utils.createOrderCode(),PeriodCheckTitle='',
                                    PeriodCheckTotalCount=0,PeriodCheckProblemsCount=0,PeriodCurrentDrugCount=currentNormalCount,
                                    PeriodCheckStatus=1,Description='',SortIndex=int(maxSortIndexRow.SortIndex or '0')+1,
                                    CreateDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),CreateUserId = user_['UserId'], 
                                    CreateUserName ='{0}({1})'.format(user_['RealName'],user_['UserCode'])
                                    )
                BllPeriodCheck().insert(entity)
            else:
                entity = BllPeriodCheck().findEntity(PeriodCheckId)
                entity.Description = Description
                entity.PeriodCheckStatus= PeriodCheckStatus
                BllPeriodCheck().update(entity)
            return JsonResponse(Utils.resultData('1', '保存成功', ''))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))

# 保存期间核查详细数据
@require_http_methods(['POST'])
@csrf_exempt
def savePeriodCheckDetailedData(request):
    try:
        if request.method == 'POST':
            PeriodCheckDetailedId = request.POST.get('PeriodCheckDetailedId','')
            PeriodCheckId = request.POST.get('PeriodCheckId','')
            DrugId = request.POST.get('DrugId','')
            Description = request.POST.get('Description','')
            Status = int(request.POST.get('Status','2'))
            PeriodCheckMethod = request.POST.get('PeriodCheckMethod','')

            periodCheckDetailedEntity=BllPeriodCheckDetailed().findEntity(and_(EntityPeriodCheckDetailed.PeriodCheckId==PeriodCheckId,
                                            EntityPeriodCheckDetailed.DrugId==DrugId))
            if(periodCheckDetailedEntity):
                PeriodCheckDetailedId=periodCheckDetailedEntity.PeriodCheckDetailedId

            periodCheckEntity=BllPeriodCheck().findEntity(PeriodCheckId)
            SQL = """SELECT max(SortIndex) as SortIndex FROM `rms_periodcheckdetailed` WHERE DrugId='"""+DrugId+"'"
            maxSortIndexRow = BllMedicament().execute(SQL).fetchone()
            user_ = request.session['login_user']
            if not PeriodCheckDetailedId:
                PeriodCheckDetailedId = str(Utils.UUID())
                
                entity = EntityPeriodCheckDetailed(PeriodCheckDetailedId=PeriodCheckDetailedId,PeriodCheckId=PeriodCheckId,DrugId=DrugId,
                                    PeriodCheckMethod=PeriodCheckMethod,Status=Status,Description=Description,
                                    SortIndex=int(maxSortIndexRow.SortIndex or '0')+1,PeriodCheckCode='',
                                    CreateDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),CreateUserId = user_['UserId'], 
                                    CreateUserName ='{0}({1})'.format(user_['RealName'],user_['UserCode'])
                                    )
                BllPeriodCheckDetailed().insert(entity)
            else:
                entity = BllPeriodCheckDetailed().findEntity(PeriodCheckDetailedId)
                entity.Description = Description
                entity.PeriodCheckMethod= PeriodCheckMethod
                entity.Status= Status
                BllPeriodCheckDetailed().update(entity)

            drugEntity=BllMedicament().findEntity(DrugId)
            drugEntity.LastPeriodCheckDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            drugEntity.LastPeriodCheckStatus=int(Status)
            BllMedicament().update(drugEntity)

            # totalCheckCount=BllPeriodCheckDetailed().findCount(EntityPeriodCheckDetailed.PeriodCheckId==PeriodCheckId)
            # problemsCount=BllPeriodCheckDetailed().findCount(and_(EntityPeriodCheckDetailed.PeriodCheckId==PeriodCheckId,EntityPeriodCheckDetailed.Status==1))
            # periodCheckEntity.PeriodCheckTotalCount=totalCheckCount
            # periodCheckEntity.PeriodCheckProblemsCount=problemsCount
            # BllPeriodCheck().update(periodCheckEntity)
            return JsonResponse(Utils.resultData('1', '保存成功', ''))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))


# 保导出PDF
@require_http_methods(['GET','POST'])
@csrf_exempt
def exportPDF(request):
    try:
        if request.method == 'POST':
            IsLandscape = int(request.POST.get('IsLandscape','0'))
            PDFHtml = request.POST.get('PDFHtml','')
            PDFName = request.POST.get('PDFName')+'.pdf'
            style='''
            <style>@media print{body{margin:0;padding:0}}@page{margin:0}.hiprint-printElement-image-content img{border:0px !important;} .hiprint-printPaper *{box-sizing:border-box;-moz-box-sizing:border-box;-webkit-box-sizing:border-box}.hiprint-printPaper *:focus{outline:-webkit-focus-ring-color auto 0}.hiprint-page-break-avoid{page-break-after:avoid}.hiprint-printPaper{position:relative;padding:0;page-break-after:always;overflow-x:hidden;overflow:hidden}.hiprint-printPaper .hiprint-printPaper-content{position:relative}.hiprint-printPaper.design{overflow:visible}.hiprint-printTemplate .hiprint-printPanel{page-break-after:always}.hiprint-printPaper,hiprint-printPanel{box-sizing:border-box;border:0}.hiprint-printPanel .hiprint-printPaper:last-child{page-break-after:avoid}.hiprint-printTemplate .hiprint-printPanel:last-child{page-break-after:avoid}.hiprint-printPaper .hideheaderLinetarget{border-top:0 dashed #c9bebe!important}.hiprint-printPaper .hidefooterLinetarget{border-top:0 dashed #c9bebe!important}.hiprint-printPaper.design{border:1px dashed rgba(170,170,170,0.7)}.design .hiprint-printElement-table-content,.design .hiprint-printElement-longText-content{overflow:hidden;box-sizing:border-box}.design .resize-panel{box-sizing:border-box;border:1px dotted}.hiprint-printElement-text{background-color:transparent;background-repeat:repeat;padding:0;border:.75pt none #000;direction:ltr;font-family:'SimSun';font-size:9pt;font-style:normal;font-weight:normal;padding-bottom:0;padding-left:0;padding-right:0;padding-top:0;text-align:left;text-decoration:none;line-height:9.75pt;box-sizing:border-box;word-wrap:break-word;word-break:break-all}.design .hiprint-printElement-text-content{border:1px dashed #cebcbc;box-sizing:border-box}.hiprint-printElement-longText{background-color:transparent;background-repeat:repeat;border:.75pt none #000;direction:ltr;font-family:'SimSun';font-size:9pt;font-style:normal;font-weight:normal;padding-bottom:0;padding-left:0;padding-right:0;padding-top:0;text-align:left;text-decoration:none;line-height:9.75pt;box-sizing:border-box;word-wrap:break-word;word-break:break-all}.hiprint-printElement-table{background-color:transparent;background-repeat:repeat;color:#000;border-color:#000;border-style:none;direction:ltr;font-family:'SimSun';font-size:9pt;font-style:normal;font-weight:normal;padding-bottom:0;padding-left:0;padding-right:0;padding-top:0;text-align:left;text-decoration:none;padding:0;box-sizing:border-box;line-height:9.75pt}.hiprint-printElement-table thead{background:#e8e8e8;font-weight:700}.hiprint-printElement-tableTarget,.hiprint-printElement-tableTarget tr,.hiprint-printElement-tableTarget td{border-color:#000;border-style:none;border:1px solid #000;font-weight:normal;direction:ltr;padding-bottom:0;padding-left:0;padding-right:0;padding-top:0;text-decoration:none;vertical-align:middle;box-sizing:border-box;word-wrap:break-word;word-break:break-all}.hiprint-printElement-tableTarget td{height:18pt}.hiprint-printPaper .hiprint-paperNumber{font-size:9pt}.design .hiprint-printElement-table-handle{position:absolute;height:21pt;width:21pt;background:red;z-index:1}.hiprint-printPaper .hiprint-paperNumber-disabled{float:right!important;right:0!important;color:gainsboro!important}.hiprint-printElement-vline,.hiprint-printElement-hline{border:0 none #000}.hiprint-printElement-vline{border-left:.75pt solid #000;border-right:0 none #000!important;border-bottom:0 none #000!important;border-top:0 none #000!important}.hiprint-printElement-hline{border-top:.75pt solid #000;border-right:0 none #000!important;border-bottom:0 none #000!important;border-left:0 none #000!important}.hiprint-printElement-oval,.hiprint-printElement-rect{border:.75pt solid #000}.hiprint-text-content-middle{display:table}.hiprint-text-content-middle>div{display:table-cell;vertical-align:middle}.hiprint-text-content-bottom{display:table}.hiprint-text-content-bottom>div{display:table-cell;vertical-align:bottom}.hi-grid-row{position:relative;height:auto;margin-right:0;margin-left:0;zoom:1;display:block;box-sizing:border-box}.hi-grid-row::after,.hi-grid-row::before{display:table;content:'';box-sizing:border-box}.hi-grid-col{display:block;box-sizing:border-box;position:relative;float:left;flex:0 0 auto}.table-grid-row{margin-left:-0pt;margin-right:-0pt}.tableGridColumnsGutterRow{padding-left:0;padding-right:0}.hiprint-gridColumnsFooter{text-align:left;clear:both}</style>
            '''
            html='<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8">'+style+'</head><body>'+PDFHtml+'</body></html>'
            path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # 安装位置
            config = pdfkit.configuration(wkhtmltopdf=path_wk)
            # with open('test.html', 'r', encoding='utf-8') as f:
            #     pdfkit.from_file(f, 'test.pdf', configuration=config)
            options = {
                'page-size': 'A4',
                'margin-top': '0mm',
                'margin-right': '0mm',
                'margin-bottom': '0mm',
                'margin-left': '0mm',
                'orientation':('Landscape' if IsLandscape==1 else 'portrait'),#横向
                'encoding': "UTF-8",
                # 'no-outline': None,
                # 'footer-right':'[page]' 设置页码
            }
            pdfkit.from_string(html,PDFName,configuration=config,options=options)
            #pdfkit.from_url('http://127.0.0.1:9000/static/666.html', 'D:/WorkData/222.pdf',configuration=config,options=options) 
            return JsonResponse(Utils.resultData('1', '保存成功', ''))
        else:
            PDFName = request.GET.get('PDFName')+'.pdf'
            response = StreamingHttpResponse(ReportData.download_excel(filename=PDFName))
            response['Content-Type'] = 'application/pdf'  # 注意格式
            response['Content-Disposition'] = 'attachment;filename=' + urlquote(PDFName)  # 注意filename 这个是下载后的名字
            response.set_cookie('fileDownload', True, 1)
            return response
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))