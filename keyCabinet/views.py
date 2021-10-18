from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import json
import base64
import copy
import pdfkit
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote
from TY_RMS_Multiple_Manage.settings import *

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
from Lib.create_barcode import CreateBarcode
from Lib.reportExcel import *
from Lib.Model import *

@require_http_methods(['GET'])
def materialStockIn(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/materialStockIn.html', locals())

@require_http_methods(['GET'])
def materialUse(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/materialUse.html', locals())

@require_http_methods(['GET'])
def materialReturn(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/materialReturn.html', locals())

@require_http_methods(['GET'])
def materialSupply(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/materialSupply.html', locals())

@require_http_methods(['GET'])
def addMaterialForm(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/addMaterialForm.html', locals())

@require_http_methods(['GET'])
def shelfSelect(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/shelfSelect.html', locals())

@require_http_methods(['GET'])
def keyCabinetSelect(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/keyCabinetSelect.html', locals())

@require_http_methods(['GET'])
def keyCabinetView(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/keyCabinetView.html', locals())

@require_http_methods(['GET'])
def mapFlowView(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/mapFlowView.html', locals())

@require_http_methods(['GET'])
def shelfUse(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/shelfUse.html', locals())

@require_http_methods(['GET'])
def shelfReturn(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/shelfReturn.html', locals())

@require_http_methods(['GET'])
def printFlowCode(request):
    if request.method == 'GET':
        return render(request, 'keyCabinet/printFlowCode.html', locals())

# 绑定模板入库
@require_http_methods(['POST'])
@csrf_exempt
def materialStockInDo(request):
    try:
        drugInfo = json.loads(request.POST.get("drugInfo","{}"))
        print(drugInfo)
        user = request.session['login_user']
        ClientId=drugInfo.get('ClientId','')
        clent=BllClient().findEntity(ClientId)
        if drugInfo['Speci'] == '':
                drugInfo['Speci'] = 0
        drugVariety = BllMedicamentVariety().createDrugVariety('', drugInfo.get('Name')
                                                                , drugInfo.get('CASNumber'), drugInfo.get('EnglishName'), drugInfo.get('Purity'),
                                                                drugInfo.get('Unit'), drugInfo.get('SpeciUnit'),
                                                                drugInfo.get('Speci'),
                                                                BllUser().findEntity(user.get('UserId')))
        drugEntity = EntityMedicament()
        drugEntity.MedicamentId = str(Utils.UUID())
        drugEntity.VarietyId = drugVariety.VarietyId
        drugEntity.BarCode = ""
        drugEntity.CustomerId = ""
        drugEntity.ClientId = ClientId
        drugEntity.CASNumber = drugInfo.get('CASNumber')
        drugEntity.Name = drugInfo.get('Name')
        drugEntity.EnglishName = drugInfo.get('EnglishName')
        drugEntity.Purity = drugInfo.get('Purity')
        drugEntity.Manufacturer = drugInfo.get('Manufacturer')
        drugEntity.Distributor = drugInfo.get('Distributor')
        drugEntity.FlowNo = FlowNo
        pDate=datetime.datetime.now()
        # if(drugInfo.get('ProductionDate','')!=''):
        #     pDate= datetime.datetime.strptime(drugInfo.get('ProductionDate'), "%Y-%m-%d")
        drugEntity.ProductionDate = pDate.strftime("%Y-%m-%d")
        # drugEntity.ShelfLife = int(drugInfo.get('ShelfLife','3650') or '3650')
        if(drugInfo.get('ExpirationDate','')!=''):
            drugEntity.ExpirationDate = datetime.datetime.strptime(drugInfo.get('ExpirationDate'), "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
        # drugEntity.ExpirationDate = (
        #             pDate + datetime.timedelta(
        #         days=drugEntity.ShelfLife)).strftime("%Y-%m-%d %H:%M:%S")
        drugEntity.InventoryWarningValue = 10
        drugEntity.ShelfLifeWarningValue = 10
        drugEntity.UseDaysWarningValue = 10
        drugEntity.FlowPositionCode = drugInfo.get('FlowPositionCode')
        drugEntity.CellPositionCode = drugInfo.get('CellPositionCode')
        drugEntity.Unit = drugInfo.get('Unit')
        drugEntity.SpeciUnit = drugInfo.get('SpeciUnit')
        drugEntity.Speci = drugInfo.get('Speci')
        drugEntity.Price = drugInfo.get('Price')
        drugEntity.Place = drugInfo.get('Place').replace('1号钥匙柜-','')
        drugEntity.IsSupervise = 0  # 默认非重点监管
        drugEntity.Remain = drugInfo.get('Speci') or '0'
        drugEntity.PutInDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        drugEntity.PutInUserId = user.get('UserId')
        drugEntity.PutInUserName = user.get('RealName')
        drugEntity.Status = 1
        drugEntity.Remark5 = drugInfo.get('Remark5') or ''
        count= int(drugInfo.get('Count','1')) or 1
        boolean_=False
        SQL = """
        SELECT MAX(BarCode+0) as StartBarCode  from RMS_Medicament
        """
        tem_obj = BllMedicament().execute(SQL).fetchone()
        max_barcode=100001
        if tem_obj is None:
            max_barcode = 100001
        else:
            max_barcode = int(tem_obj.StartBarCode+1)
            if(int(max_barcode)<100001):
                max_barcode = 100001
        for i in range(count):
            drugEntity1=copy.deepcopy(drugEntity)
            drugEntity1.MedicamentId = str(Utils.UUID())
            if(drugInfo.get('CellPositionCode')==101):
                drugEntity1.BarCode = max_barcode+i
            boolean_ = BllMedicament().drugPutIn(drugEntity1, clent,
                                        BllUser().findEntity(user.get('UserId')))
        if boolean_:
            print('ggggggggggggggggggggg:',drugInfo.get('CellPositionCode'))
            if(drugInfo.get('CellPositionCode')==101):
                for barcode in range(max_barcode, max_barcode+count):
                    CreateBarcode().create_Code128_img(str(barcode))
                    time.sleep(0.1)
            return JsonResponse(Utils.resultData(0, '试剂入库成功！'))
        else:
            return JsonResponse(Utils.resultData(1, '数据异常，入库失败！'))
    except Exception as e:
        print(e, 888888888888)
        return JsonResponse(Utils.resultData(1, '数据异常, 入库失败！'))

@require_http_methods(['GET'])
def getSupplyDrugCategoryListJson(request):
    if request.method == 'GET':
        page = int(request.GET.get("page", '1'))
        limit = int(request.GET.get("limit", '15'))
        pageParam=PageParam(page, limit)
        drug_list = BllMedicamentVariety().getSupplyDrugCategoryList(pageParam)
        return JsonResponse({'data': drug_list,'code' : 0,'msg':'','count':pageParam.totalRecords})