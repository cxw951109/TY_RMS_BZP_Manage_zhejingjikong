from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from Lib.searchDrug import GetDrugTypeData
from Lib.Utils import *
from Lib.create_barcode import CreateBarcode
from django.views.decorators.csrf import csrf_exempt

import json
import time
import datetime

from Business.BllMedicamentTemplate import *
from Business.BllMedicament import *
from Business.BllUser import *
from Business.BllClient import *
from Lib.readExcel import *


# 新增模板条目 输入试剂名称自动搜索试剂列表处理函数
@require_http_methods(['GET'])
def autoSearchDrugList(request):
    if request.method == 'GET':
        time1 = time.time()
        CASNumber = request.GET.get('CASNumber', '')
        if not CASNumber:
            search_word = request.GET.get('keyWord')
            data_list = GetDrugTypeData.search_data(search_word)
            time2 = time.time()
            return JsonResponse(data_list, safe=False)
        else:
            logger.info('CASNumber被传入值')
            return JsonResponse([], safe=False)


# RFID试剂入库视图处理函数
def RFIDStorage(request, template_id):
    # 声明一个列表用来存放所有的TemplateContent的子模板
    all_children_template_list = []
    template_id = template_id
    template_obj = BllMedicamentTemplate().findEntity(template_id)
    # 把获取到的TemplateContent 字符串转化为 list
    TemplateContent_list = eval(json.loads(Utils.resultAlchemyData(template_obj))['TemplateContent'])
    # 如果TemplateContent 子模板ExportCount 里面的数量大于1 数量为多少则存放多少个子模板
    for template_content in TemplateContent_list:
        # 获取子模板存放的数量
        count = int(template_content['ExportCount'])
        while count:
            all_children_template_list.append(template_content)
            count -= 1
    # 获取client_id ， CustomerId的值
    request.session['template_list'] = all_children_template_list
    client_id = json.loads(Utils.resultAlchemyData(template_obj))['ClientId']
    CustomerId = json.loads(Utils.resultAlchemyData(template_obj))['CustomerId']
    return render(request, 'drugTemplate/RFIDStorage.html', locals())


# 绑定模板入库
@csrf_exempt
def bind_template(request):
    try:
        time.sleep(0.5)
        template_index = request.POST.get('template_index')
        CustomerId = request.POST.get('CustomerId')
        if CustomerId == 'None':
            CustomerId = ''
        ClientId = request.POST.get('client_id')
        RFID = request.POST.get('RFID')
        if RFID == "" or RFID is None:
            return JsonResponse({'data': Utils.resultData(1, 'RFID不能为空！')})
        # 获取存储的session  template_list 根据前段传来的值判断取第几个模板
        if(int(template_index) >= len(request.session['template_list'])):
            return JsonResponse({'data': Utils.resultData(1, '该模板已被全部绑定！')})
        drugInfo = request.session['template_list'][int(template_index)]
        # 获取存储的user
        user = request.session['login_user']
        drugEntity = BllMedicament().findEntity(EntityMedicament.BarCode == RFID)
        if (drugEntity is not None):
            return JsonResponse({'data': Utils.resultData(1, '该试剂已被绑定！')})
        else:
            if drugInfo['Speci'] == '':
                drugInfo['Speci'] = 0
            drugVariety = BllMedicamentVariety().createDrugVariety(CustomerId, drugInfo.get('Name')
                                                                   , drugInfo.get('CASNumber'), drugInfo.get('EnglishName'), drugInfo.get('Purity'),
                                                                   drugInfo.get('Unit'), drugInfo.get('SpeciUnit'),
                                                                   drugInfo.get('Speci'),
                                                                   BllUser().findEntity(user.get('UserId')))
            drugEntity = EntityMedicament()
            drugEntity.MedicamentId = str(Utils.UUID())
            drugEntity.VarietyId = drugVariety.VarietyId
            drugEntity.BarCode = RFID
            drugEntity.CustomerId = CustomerId
            drugEntity.ClientId = ClientId
            drugEntity.CASNumber = drugInfo.get('CASNumber')
            drugEntity.Name = drugInfo.get('Name')
            drugEntity.EnglishName = drugInfo.get('EnglishName')
            drugEntity.Purity = drugInfo.get('Purity')
            drugEntity.Manufacturer = drugInfo.get('Manufacturer')
            drugEntity.Distributor = drugInfo.get('Distributor')
            drugEntity.ProductionDate = drugInfo.get('ProductionDate')
            drugEntity.ShelfLife = int(drugInfo.get('ShelfLife'))
            drugEntity.ExpirationDate = (
                        datetime.datetime.strptime(drugInfo.get('ProductionDate'), "%Y-%m-%d") + datetime.timedelta(
                    days=drugEntity.ShelfLife)).strftime("%Y-%m-%d %H:%M:%S")
            drugEntity.InventoryWarningValue = 10
            drugEntity.ShelfLifeWarningValue = 10
            drugEntity.UseDaysWarningValue = 10
            drugEntity.Unit = drugInfo.get('Unit')
            drugEntity.SpeciUnit = drugInfo.get('SpeciUnit')
            drugEntity.Speci = drugInfo.get('Speci')
            drugEntity.Price = drugInfo.get('Price')
            drugEntity.Place = drugInfo.get('Place')
            drugEntity.IsSupervise = 0  # 默认非重点监管
            drugEntity.Remain = drugInfo.get('Speci')
            drugEntity.PutInDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            drugEntity.PutInUserId = user.get('UserId')
            drugEntity.PutInUserName = user.get('RealName')
            drugEntity.Status = 5

            boolean_ = BllMedicament().drugPutIn(drugEntity, BllClient().findEntity(ClientId),
                                      BllUser().findEntity(user.get('UserId')))
            # retrunData = Utils.resultData(0,'试剂入库成功！',drugEntity)
            if boolean_:
                return JsonResponse({'data': Utils.resultData(0, '试剂入库成功！')})
            else:
                return JsonResponse({'data': Utils.resultData(1, '数据异常，入库失败！')})

    except Exception as e:
        print(e, 888888888888)
        return JsonResponse({'data': Utils.resultData(1, '数据异常, 入库失败！')})


# 打印模板绑定试剂条码处理函数
def printer_drug_code(request):
    try:
        TemplateId = request.GET.get('TemplateId', '')
        if TemplateId:
            tem_obj = BllMedicamentTemplate().findEntity(TemplateId)
            # 获取endBarCode进行遍历  一次打印条码  for循环不包括最后一位正好
            endBarCode = int(tem_obj.StartBarCode) + tem_obj.BarCodeCount
            for barcode in range(tem_obj.StartBarCode, endBarCode):
                CreateBarcode().create_Code128_img(str(barcode))
                time.sleep(0.1)
            return JsonResponse({'data': Utils.resultData(0, '打印成功！')})
    except Exception as e:
        print(e)
        return JsonResponse({'data': Utils.resultData(1, '打印失败，数据异常！')})

#导入入库模板
@require_http_methods(['GET'])
def exportPutInTemplate(request):
        try:
            file_path = Utils.getUDiskPath()
            print(file_path)
            if file_path:
                ClientId = request.GET.get('ClientId', '')
                print(ClientId)
                a = ReadExcel(file_path + '/reagentTemplate.xlsx')
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
                result_list = a.read()
                print(result_list, 9999999999999)
                client=BllClient().findEntity(ClientId)
                print('fffffffff')
                user = request.session['login_user']
                user = BllUser().findEntity(user['UserId'])
                if result_list is not None:
                    medicament_obj_list = []
                    for value in result_list:
                        totalCount=0
                        TemplateContent_list = eval(value)
                        # 如果TemplateContent 子模板ExportCount 里面的数量大于1 数量为多少则存放多少个子模板
                        for template_content in TemplateContent_list:
                            # 获取子模板存放的数量
                            totalCount+= int(template_content['ExportCount'])
                        medicament_obj = EntityMedicamentTemplate(
                            TemplateId=str(Utils.UUID()), CustomerId=client.CustomerId, ClientId=client.ClientId, ClientName=client.ClientName,
                            TemplateName='入库模板_'+Utils.getFileName(), TemplateContent=value, IsWaitExport=1,StartBarCode=str(StartBarCode), BarCodeCount=totalCount,
                            CreateDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),CreateUserId=user.UserId,CreateUserName=user.RealName,
                        )
                        medicament_obj_list.append(medicament_obj)
                    status = BllMedicamentTemplate().insert_many(medicament_obj_list)
                    if status:
                        return JsonResponse({'data': Utils.resultData(0, '导入成功！')})
                    else:
                        return JsonResponse({'data': Utils.resultData(1, '入库单异常, 导入失败！')})
                else:
                    return JsonResponse({'data': Utils.resultData(1, '入库单格式不正确, 请检查之后重新导入！')})
            else:
                return JsonResponse({'data': Utils.resultData(1, '请插入U盘！')})
        except FileNotFoundError as e:
            return JsonResponse({'data': Utils.resultData(1, '当前U盘下暂无reagentTemplate.xlsx文件！')})
        except Exception as e:
            print(e)
            return JsonResponse({'data': Utils.resultData(1, '模板错误：'+str(e))})

