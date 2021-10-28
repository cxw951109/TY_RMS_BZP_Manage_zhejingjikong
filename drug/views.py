import json
import threading
from dwebsocket.decorators import accept_websocket

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Business.BllClient import BllClient
from Business.BllMedicament import *
from Business.BllUser import *
from Business.BllUserMedicament import *
from Business.BllApproveInfo import *
from DataEntity.EntityMedicamentVariety import *
from Lib.Balance import Balance
from Lib.RFIDDevice import RFIDDevice
from Lib.Utils import logger
from Lib.Model import *
from TY_RMS_Multiple_Manage.AccuLockTcpServer import *
from Business.BllMedicament import *

try:
    RFID_cls = RFIDDevice()
except Exception as e:
    print(e, 'RFID 通讯失败...')


@require_http_methods(['GET', "POST"])
@csrf_exempt
def danger(request):
    if request.method == 'GET':
        return render(request, 'danger/danger.html', locals())
    else:
        name = str(request.POST["name"])
        jsonData = BllMedicament().select_danger(name)
        return JsonResponse(Utils.resultAlchemyData(jsonData), safe=False)


# 删除选中试剂视图处理函数, 并跳过csrf验证
@require_http_methods(['POST'])
@csrf_exempt
def deleteDrug(request):
    if request.method == 'POST':
        try:
            MedicamentId = request.POST['MedicamentId']
            medicament_obj = BllMedicament().findEntity(MedicamentId)
            if medicament_obj.Status == 2:
                return JsonResponse(Utils.resultData('0', '当前试剂未在库, 禁止删除！'))
            elif medicament_obj.Status == 3:
                medicamentVa_obj = BllMedicamentVariety().findEntity(medicament_obj.VarietyId)
                if medicamentVa_obj:
                    medicamentVa_obj.EmptyCount -= 1
                    BllMedicamentVariety().update(medicamentVa_obj)

            BllMedicament().delete_drug(MedicamentId=MedicamentId, medicament_obj=medicament_obj)
            return JsonResponse(Utils.resultData('1', '删除成功', ''))
        except Exception as e:
            print(e)
            return JsonResponse(Utils.resultData('0', e, ''))


# 设置选中试剂空瓶视图处理函数, 并跳过csrf验证
@require_http_methods(['POST'])
@csrf_exempt
def setDrugEmpty(request):
    if request.method == 'POST':
        try:
            user_ = request.session['login_user']
            MedicamentId = request.POST['MedicamentId']
            medicament_obj = BllMedicament().findEntity(MedicamentId)
            ApproveContent = "申请销毁试剂“{0}({1})”".format(medicament_obj.Name, medicament_obj.BarCode)
            BllApproveInfo().addApproveInfo(ApproveTypeAllCode.DrugDestroy, ApproveContent, medicament_obj.MedicamentId,
                                            medicament_obj.BarCode, '', user_['UserId'])
            # if(medicament_obj.Status!=3):
            #     medicament_obj.Status=3
            #     BllMedicament().update(medicament_obj)
            #     medicament_obj = BllMedicament().findEntity(MedicamentId)
            #     user=BllUser().findEntity(request.session['login_user'].get('UserId'))
            #     BllMedicament().drugReturn(medicament_obj,None,user)
            return JsonResponse(Utils.resultData('1', '申请成功', ''))
        except Exception as e:
            print(e)
            return JsonResponse(Utils.resultData('0', '数据异常', ''))


# 设置试剂图片
@require_http_methods(['POST'])
@csrf_exempt
def setDrugImageUrl(request):
    if request.method == 'POST':
        try:
            MedicamentId = request.POST['MedicamentId']
            ImageUrl = request.POST['ImageUrl']
            medicament_obj = BllMedicament().findEntity(MedicamentId)
            medicament_obj.ImageUrl = ImageUrl
            BllMedicament().update(medicament_obj)
            return JsonResponse(Utils.resultData('1', '设置成功', ''))
        except Exception as e:
            print(e)
            return JsonResponse(Utils.resultData('0', '数据异常', ''))


# 设置试剂图片
@require_http_methods(['POST'])
@csrf_exempt
def getDrugImageUrl(request):
    if request.method == 'POST':
        try:
            MedicamentId = request.POST['MedicamentId']
            ImageUrl = request.POST['ImageUrl']
            medicament_obj = BllMedicament().findEntity(MedicamentId)
            medicament_obj.ImageUrl = ImageUrl
            BllMedicament().update(medicament_obj)
            return JsonResponse(Utils.resultData('1', '设置成功', ''))
        except Exception as e:
            print(e)
            return JsonResponse(Utils.resultData('0', '数据异常', ''))


# 请求试剂类型处理函数
@require_http_methods(['GET'])
def drugTypeIndex(request):
    if request.method == 'GET':
        searchValue = request.GET.get('searchValue', '')
        return render(request, 'drug/drugTypeIndex.html', locals())


@require_http_methods(['GET'])
def getDrugTypeListJson(request):
    if request.method == 'GET':
        searchValue = request.GET['searchValue']
        if not searchValue:
            data = BllMedicamentVariety().findList().order_by(desc(EntityMedicamentVariety.CreateDate)).all()
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data))})
        data = BllMedicamentVariety().findEnglishOrChinseNameList(searchValue).order_by(
            desc(EntityMedicamentVariety.CreateDate)).all()
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data))})


# 创建试剂实体类
@require_http_methods(['POST'])
@csrf_exempt
def createDrugType(request):
    if request.method == 'POST':
        CustomerId = request.session['login_user'].get('CustomerId')
        VarietyId = request.POST['VarietyId']
        Name = request.POST['Name']
        EnglishName = request.POST['EnglishName']
        CASNumber = request.POST['CASNumber']
        Purity = request.POST['Purity']
        InventoryWarningValue = request.POST['InventoryWarningValue']
        ShelfLifeWarningValue = request.POST['ShelfLifeWarningValue']
        UseDaysWarningValue = request.POST['UseDaysWarningValue']
        Remark1 = request.POST['Remark1']
        Remark2 = request.POST['Remark2']
        Remark3 = request.POST['Remark3']
        IsSupervise = request.POST['IsSupervise']
        IsWeigh = request.POST['IsWeigh']
        # 根据VarietyId是否有值判断是创建新的试剂类别还是修改
        if not VarietyId:
            VarietyId = str(Utils.UUID())
            BllMedicamentVariety_obj = BllMedicamentVariety().findList(EntityMedicamentVariety.Name == Name,
                                                                       EntityMedicamentVariety.EnglishName == EnglishName).all()

            if not BllMedicamentVariety_obj:
                user = request.session['login_user']
                medicamentVariety = EntityMedicamentVariety(VarietyId=VarietyId, Name=Name, EnglishName=EnglishName,
                                                            CASNumber=CASNumber, Purity=Purity, Remark1=Remark1,
                                                            EmptyCount=0,
                                                            UseCount=0, NormalCount=0, TotalCount=0,
                                                            CreateUserId=user['UserId'],
                                                            CreateUserName=user['RealName'],
                                                            InventoryWarningValue=InventoryWarningValue,
                                                            Remark2=Remark2,
                                                            ShelfLifeWarningValue=ShelfLifeWarningValue,
                                                            Remark3=Remark3,
                                                            UseDaysWarningValue=UseDaysWarningValue,
                                                            CustomerId=CustomerId,
                                                            IsSupervise=IsSupervise,
                                                            CreateDate=datetime.datetime.now().strftime(
                                                                '%Y-%m-%d %H:%M:%S')
                                                            )

                BllMedicamentVariety().insert(medicamentVariety)
                return JsonResponse(Utils.resultData('1', '保存成功', ''))
            else:
                return JsonResponse(Utils.resultData('0', '该类别已经存在，请换个类别试试吧！', ''))
        else:
            medicamentVariety = BllMedicamentVariety().findEntity(VarietyId)
            medicamentVariety.Name = Name
            medicamentVariety.EnglishName = EnglishName
            medicamentVariety.CASNumber = CASNumber
            medicamentVariety.Purity = Purity
            medicamentVariety.InventoryWarningValue = InventoryWarningValue
            medicamentVariety.ShelfLifeWarningValue = ShelfLifeWarningValue
            medicamentVariety.UseDaysWarningValue = UseDaysWarningValue
            medicamentVariety.Remark1 = Remark1
            medicamentVariety.Remark2 = Remark2
            medicamentVariety.Remark3 = Remark3
            medicamentVariety.IsSupervise = IsSupervise
            medicamentVariety.IsWeigh = IsWeigh
            BllMedicamentVariety().update(medicamentVariety)
            # SQL查询保质期预警数量
            SQL = """
            update rms_medicament set ShelfLifeWarningValue=""" + ShelfLifeWarningValue + """ ,IsWeigh=""" + IsWeigh + """  where VarietyId='""" + VarietyId + """';
            """
            print(SQL)
            BllMedicament().executeNoParam(SQL)
            return JsonResponse(Utils.resultData('1', '修改成功', ''))


@require_http_methods(['GET'])
def drugEditorTypeForm(request, varietyId):
    if request.method == 'GET':
        drugType_obj = BllMedicamentVariety().findEntity(varietyId)
        return render(request, 'drug/drugTypeForm.html', locals())


@require_http_methods(['POST'])
@csrf_exempt
def deleteDrugType(request):
    if request.method == 'POST':
        varietyId = request.POST['varietyId']
        BllMedicamentVariety().delete(EntityMedicamentVariety.VarietyId == varietyId)
        return JsonResponse(Utils.resultData('1', '删除成功', ''))


# 获取扫码查询的数据
def GetDrugJson(request):
    drug_id = request.GET.get('drugId', '')
    if drug_id:
        medicament_obj = BllMedicament().findEntity(EntityMedicament.BarCode == drug_id)
        print(medicament_obj)
        if medicament_obj:
            medicament_obj = Utils.resultAlchemyData(medicament_obj)
            return JsonResponse({'data': Utils.resultData(1, '获取成功', data=medicament_obj)})
        else:
            return JsonResponse({'data': Utils.resultData(0, '该试剂编号没有入库')})
    else:
        return JsonResponse({'data': Utils.resultData(0, '没有获取到该编号')})


# 获取待归还试剂
def getWaitRetrunDrugList(request):
    currentInfoJsonStr = request.session['login_user']
    retrunData = ''
    try:
        drugList = BllMedicament().getWaitReturnDrugList(currentInfoJsonStr.get("CustomerId"))
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(drugList))})
    except Exception as e:
        logger.debug('数据库操作失败')
        BllMedicament().session.rollback()


# 扫码获取信息并且称重
def GetDrugJsonAndWeight(request):
    drug_id = request.GET.get('drugId', '')
    if drug_id:
        medicament_obj = BllMedicament().findEntity(EntityMedicament.BarCode == drug_id)
        if medicament_obj:
            try:
                a = Balance()
            except:
                return JsonResponse({'data': Utils.resultData(0, '通讯失败，请检查串口是否连接！')})

            a.write('#')
            drug_margin = a.read()
            if drug_margin:
                if drug_margin[0] == '+':
                    drug_margin = drug_margin[1:]
                    # 将称重的数据赋值给查询到的试剂余量
                    medicament_obj.Remain = drug_margin
                    print(medicament_obj, 8888888888888)
                    medicament_obj = Utils.resultAlchemyData(medicament_obj)
                    return JsonResponse({'data': Utils.resultData(1, '修改成功', data=medicament_obj)})
                else:
                    return JsonResponse({'data': Utils.resultData(0, '余量为负， 请校准天平！')})
            else:
                return JsonResponse({'data': Utils.resultData(0, '天平数据未获取到，请重试！')})

        else:
            return JsonResponse({'data': Utils.resultData(0, '该试剂编号没有入库！')})
    else:
        return JsonResponse({'data': Utils.resultData(0, '没有获取到该编号')})


# 试剂归还视图处理
@csrf_exempt
def drug_weigh(request):
    if request.method == 'GET':
        return render(request, 'drug/drug_weigh.html', locals())
    elif request.method == 'POST':
        # 获取试剂余量
        remain = float(request.POST.get('drug_margin'))
        # 获取试剂ID
        drug_id = request.POST.get('drug_id')
        drug_obj = BllMedicament().findEntity(drug_id)
        if drug_obj:
            # if remain > float(drug_obj.Remain)+0.5:
            #     return JsonResponse({'data': Utils.resultData(0, '当前称重质量'+ str(remain)+'g大于历史质量')})
            drug_obj.Remain = remain  # 余量
            drug_obj.WeighFlag = 1
            # if remain == 0:
            #     drug_obj.Status = 3
            #     user_ = request.session['login_user']
            #     entity_obj = EntityMedicamentRecord(RecordId=str(Utils.UUID()), ClientId=drug_obj.ClientId,
            #                                         ClientCode=drug_obj.ClientCode, CustomerId=drug_obj.CustomerId,
            #                                         VarietyId=drug_obj.VarietyId, MedicamentId=drug_obj.MedicamentId,
            #                                         RecordType=3, Price=drug_obj.Price, IsEmpty=1,
            #                                         CreateDate=datetime.datetime.now(), CreateUserId=user_['UserId'],
            #                                         CreateUserName=user_['RealName'], IsAdd=1)
            #     BllMedicamentRecord().insert(entity_obj)
            if remain < 0:
                return JsonResponse({'data': Utils.resultData(0, '请查看天平是否校准，余量为负！')})
            bool_ = BllMedicament().update(drug_obj)
            drug_obj = Utils.resultAlchemyData(drug_obj)  # 格式化entity对象
            if bool_:
                return JsonResponse({'data': Utils.resultData(1, '保存成功！', data=drug_obj)})
            else:
                return JsonResponse({'data': Utils.resultData(0, '数据异常，保存失败！')})
        else:
            return JsonResponse({'data': Utils.resultData(0, '该RFID未入库！')})


# 天平去皮
def balance_tare(request):
    if request.method == 'GET':
        try:
            a = Balance()
        except:
            return JsonResponse({'data': Utils.resultData(0, '通讯失败，请检查串口是否连接！')})

        a.write('T')
        return JsonResponse({'data': Utils.resultData(1, '成功')})


# 获取指定归还RFID试剂信息
def GetDrugInfo(request):
    if request.method == 'GET':
        drug_id = request.GET.get('drugId', '')

        if drug_id:
            medicament_obj = BllMedicament().findEntity(EntityMedicament.BarCode == drug_id)
            if medicament_obj:
                if medicament_obj.Status == 2 or medicament_obj.Status == 5:
                    medicament_obj = Utils.resultAlchemyData(medicament_obj)
                    try:
                        a = Balance()
                    except:
                        return JsonResponse({'data': Utils.resultData(0, '通讯失败，请检查串口是否连接！')})

                    a.write('#')
                    drug_margin = a.read()
                    if drug_margin:
                        if drug_margin[0] == '+':
                            drug_margin = drug_margin[1:]
                        else:
                            return JsonResponse({'data': Utils.resultData(0, '余量为负， 请校准天平！')})
                        return JsonResponse(
                            {'data': Utils.resultData(1, '获取成功', data=medicament_obj), 'drug_margin': drug_margin})

                    else:
                        return JsonResponse({'data': Utils.resultData(0, '天平数据未获取到，请重试！')})
                elif medicament_obj.Status == 3:
                    return JsonResponse({'data': Utils.resultData(0, '该试剂当前状态为空瓶，禁止修改！')})
                else:
                    return JsonResponse({'data': Utils.resultData(0, '该试剂当前状态为在库，请核对药柜信息！')})
            else:
                return JsonResponse({'data': Utils.resultData(0, '该RFID编号不存在！')})

        else:
            return JsonResponse({'data': Utils.resultData(0, '数据异常, 没有获取到试剂！')})


@accept_websocket
def drug_socket(request):
    if request.is_websocket():
        try:
            while 1:
                message = request.websocket.wait()  # 接受前段发送来的数据
                if message:
                    message = bytes.decode(message)
                    if message != '886':
                        try:
                            receive_data = RFID_cls.getRFID()
                            if receive_data:
                                request.websocket.send(receive_data.encode())  # 发送给前段的数据


                        except Exception as e:
                            print(e, 33333333333333333)
                            request.websocket.close()
                            return
                    else:
                        print('socket请求关闭！！！')
                        request.websocket.close()
                        return
                else:
                    print('socket请求关闭！！！')
                    request.websocket.close()
                    return

        except Exception as e:
            try:
                print(e)
                request.websocket.close()
                return
            except Exception as e:
                print(e)
                return


# 试剂禁止使用用户
def disabled_user(request):
    if request.method == 'GET':
        barcode = request.GET.get('barcode', '')
        if barcode:
            drug_obj = BllMedicament().findEntity(EntityMedicament.BarCode == barcode)
            print(drug_obj, 888888888)
            user_list = BllUser().findList().all()
            BllUserMedicament_obj_list = BllUserMedicament().findList(
                EntityUserMedicament.DrugId == drug_obj.MedicamentId).all()
            # 获取已经被禁用的用户列表
            disabled_user_list = []
            for BllUserMedicament_obj in BllUserMedicament_obj_list:
                disabled_user_list.append(BllUserMedicament_obj.UserId)
            drugId = drug_obj.MedicamentId
            print(drugId)
            return render(request, 'drug/disabled_user.html', locals())


@csrf_exempt
def saveDisabledUser(request):
    if request.method == 'POST':
        drugId = request.POST.get('drugId', '')
        powerValue = request.POST.get('powerValue', '').split(',')
        print(drugId, powerValue, 8888888888888888888)
        if drugId:
            BllUserMedicament().delete(EntityUserMedicament.DrugId == drugId)
            for user_id in powerValue:
                client_user_obj = BllUserMedicament().findEntity(and_(EntityUserMedicament.UserId == user_id,
                                                                      EntityUserMedicament.DrugId == drugId))
                if client_user_obj:
                    continue
                disabled_obj = EntityUserMedicament(Id=str(Utils.UUID()), UserId=user_id, DrugId=drugId)
                BllUserMedicament().insert(disabled_obj)
            return JsonResponse(Utils.resultData('1', '保存成功！'))
        else:
            return JsonResponse(Utils.resultData('0', '试剂未获取到！'))


############################以下为测试代码以废弃###########################################
# @csrf_exempt
# def drugPutInView__(request):
#     if request.method == 'GET':
#         return render(request, 'drug/DrugPutInByBarCode.html', locals())
#     elif request.method == 'POST':
#         print("17来访问了....................................................................")
#         template_index = request.POST.get('template_index')
#         userInfo = request.session['login_user']
#         customerId = request.POST.get('CustomerId')

#         barCode = request.POST.get("barCode")
#         clientId = request.POST.get("client_id")
#         clientEntity = BllClient().findEntity(EntityClient.ClientId == clientId)
#         print("展示CustomerId:",clientEntity.CustomerId)

#         # 获取存储的session  template_list 根据前段传来的值判断取第几个模板
#         if(int(template_index) >= len(request.session['template_list'])):
#             return JsonResponse({'data': Utils.resultData(1, '该模板已被全部绑定！')})
#         drugInfo = request.session['template_list'][int(template_index)]

#         drugEntity = BllMedicament().findEntity(EntityMedicament.BarCode == barCode)
#         if(drugEntity is not None):
#             retrunData = Utils.resultData(1,'此条码已被绑定！')
#         else:
#             if drugInfo['Speci'] == '':
#                 drugInfo['Speci'] = 0
#             drugVariety = BllMedicamentVariety().createDrugVariety(customerId,drugInfo.get('Name'),drugInfo.get('EnglishName')
#                                                         ,drugInfo.get('CASNumber'),drugInfo.get('Purity'),drugInfo.get('Unit'),drugInfo.get('SpeciUnit'),drugInfo.get('Speci'),BllUser().findEntity(userInfo.get('UserId')))
#             drugEntity = EntityMedicament()
#             drugEntity.MedicamentId = Utils.UUID()
#             drugEntity.VarietyId = drugVariety.VarietyId
#             drugEntity.BarCode = barCode
#             drugEntity.CustomerId = customerId
#             drugEntity.ClientId = request.POST.get('client_id')
#             drugEntity.ClientCode = clientEntity.ClientCode
#             drugEntity.CASNumber = drugInfo.get('CASNumber')
#             drugEntity.Name = drugInfo.get('Name')
#             drugEntity.EnglishName = drugInfo.get('EnglishName')
#             drugEntity.Purity = drugInfo.get('Purity')
#             drugEntity.Manufacturer = drugInfo.get('Manufacturer')
#             drugEntity.Distributor = drugInfo.get('Distributor')
#             drugEntity.ProductionDate = drugInfo.get('ProductionDate')
#             drugEntity.ShelfLife = int(drugInfo.get('ShelfLife'))
#             drugEntity.ExpirationDate = (datetime.datetime.strptime(drugInfo.get('ProductionDate'), "%Y-%m-%d") + datetime.timedelta(days = drugEntity.ShelfLife)).strftime("%Y-%m-%d %H:%M:%S")
#             drugEntity.InventoryWarningValue = 10
#             drugEntity.ShelfLifeWarningValue = 10
#             drugEntity.UseDaysWarningValue = 10
#             drugEntity.Unit = drugInfo.get('Unit')
#             drugEntity.SpeciUnit = drugInfo.get('SpeciUnit')
#             drugEntity.Speci = drugInfo.get('Speci')
#             drugEntity.Price = drugInfo.get('Price')
#             drugEntity.Place = drugInfo.get('Place')
#             drugEntity.Remain = drugInfo.get('Remain') ###不知道模板中是否有--待确认
#             drugEntity.PutInDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             drugEntity.PutInUserId = userInfo.get('UserId')
#             drugEntity.PutInUserName = userInfo.get('UserRealName')
#             drugEntity.Status = DrugStatus.Normal
#             # entityClient = BllClient().findEntity(request.POST.get('ClientId'))
#             BllMedicament().drugPutIn(drugEntity,clientEntity,BllUser().findEntity(userInfo.get('UserId')))
#             # retrunData = Utils.resultData(0,'试剂入库成功！',drugEntity)
#             print('石棋几乎以为他要成功了......................')
#             retrunData = Utils.resultData(0,'试剂入库成功！')
#         return JsonResponse(retrunData)
############################以上为测试代码以废弃##########################################

# 试剂扫一维条码入库处理视图
@csrf_exempt
def drugPutInView(request):
    import random
    if request.method == 'GET':
        return render(request, 'drug/DrugPutInByBarCode.html', locals())
    elif request.method == 'POST':
        template_index = request.POST.get('template_index')
        userInfo = request.session['login_user']
        customerId = request.POST.get('CustomerId')
        barCode = request.POST.get("barCode")
        clientId = request.POST.get("client_id")
        clientEntity = BllClient().findEntity(EntityClient.ClientId == clientId)
        # 获取存储的session  template_list 根据前段传来的值判断取第几个模板
        if (int(template_index) >= len(request.session['template_list'])):
            retrunData = Utils.resultData(1, '该模板已被全部绑定！')
            return JsonResponse(retrunData)
        drugInfo = request.session['template_list'][int(template_index)]
        # try:
        drugEntity = BllMedicament().findEntity(EntityMedicament.BarCode == barCode)
        if (drugEntity is not None):
            retrunData = Utils.resultData(1, '此条码已被绑定！')
        else:
            if drugInfo['Speci'] == '':
                drugInfo['Speci'] = 0
            drugVariety = BllMedicamentVariety().createDrugVariety(customerId, drugInfo.get('Name'),
                                                                   drugInfo.get('EnglishName')
                                                                   , drugInfo.get('CASNumber'), drugInfo.get('Purity'),
                                                                   drugInfo.get('Unit'), drugInfo.get('SpeciUnit'),
                                                                   drugInfo.get('Speci'),
                                                                   BllUser().findEntity(userInfo.get('UserId')))
            drugEntity = EntityMedicament()
            drugId = Utils.UUID()
            drugEntity.MedicamentId = drugId
            drugEntity.VarietyId = drugVariety.VarietyId
            # drugEntity.BarCode = barCode
            drugEntity.BarCode =str(random.randint(10000000,99999999))
            drugEntity.CustomerId = customerId
            drugEntity.ClientId = clientEntity.ClientId
            drugEntity.ClientCode = clientEntity.ClientCode
            drugEntity.CASNumber = drugInfo.get('CASNumber', '')
            drugEntity.Name = drugInfo.get('Name', '')
            drugEntity.EnglishName = drugInfo.get('EnglishName', '')
            drugEntity.Purity = drugInfo.get('Purity', '')
            drugEntity.Manufacturer = drugInfo.get('Manufacturer', '')
            drugEntity.Distributor = drugInfo.get('Distributor', '')
            productionDate = drugInfo.get('ProductionDate') or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            drugEntity.ProductionDate = productionDate[:10]
            drugEntity.ShelfLife = int(drugInfo.get('ShelfLife') or '6000')
            drugEntity.ExpirationDate = (
                        datetime.datetime.strptime(productionDate[:10], "%Y-%m-%d") + datetime.timedelta(
                    days=drugEntity.ShelfLife)).strftime("%Y-%m-%d %H:%M:%S")
            drugEntity.InventoryWarningValue = 10
            drugEntity.ShelfLifeWarningValue = 10
            drugEntity.UseDaysWarningValue = 10
            drugEntity.Unit = drugInfo.get('Unit', '')
            drugEntity.SpeciUnit = drugInfo.get('SpeciUnit', '')
            drugEntity.Speci = float(drugInfo.get('Speci') or '0')
            drugEntity.Price = float(drugInfo.get('Price') or '0')
            drugEntity.Place = drugInfo.get('Place', '')
            drugEntity.Remain = float(drugInfo.get('Remain') or '0')  ###不知道模板中是否有--待确认
            drugEntity.PutInDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            drugEntity.PutInUserId = userInfo.get('UserId', '')
            drugEntity.PutInUserName = userInfo.get('RealName', '')
            drugEntity.Remark1 = drugInfo.get('Remark1', '')
            drugEntity.Remark2 = drugInfo.get('Remark2', '')
            drugEntity.Remark3 = drugInfo.get('Remark3', '')
            drugEntity.Remark4 = drugInfo.get('Remark4', '')
            drugEntity.Remark5 = drugInfo.get('Remark5', '')
            drugEntity.Remark6 = drugInfo.get('Remark6', '')
            drugEntity.Remark7 = drugInfo.get('Remark7', '')
            drugEntity.Remark8 = drugInfo.get('Remark8', '')
            drugEntity.Remark9 = drugInfo.get('Remark9', '')
            drugEntity.Remark10 = drugInfo.get('Remark10', '')
            drugEntity.Status = DrugStatus.Normal

            client_obj = BllClient().findEntity(clientId)
            datalist = BllMedicament().get_boxlist(clientId,type='up',num=1)
            if datalist != False:
                BllMedicament().drugPutIn(drugEntity, clientEntity, BllUser().findEntity(userInfo.get('UserId')))
                AccuLockTcpServer.Data={"terminal":client_obj.ClientName,"mes":'lighton'+'~'.join(datalist)}
                print('入库亮灯:','lighton'+"~".join(datalist))
                retrunData = Utils.resultData(0, '试剂入库成功！', data=datalist[0])
            else:
                retrunData = Utils.resultData(1, '柜子已满！', data=[])

        # except Exception as e:
        #     print(e)
        #     retrunData = Utils.resultData(1,str(e))
        return JsonResponse(retrunData)


# 试剂领用处理视图
@csrf_exempt
def drugUseView(request):
    if request.method == 'GET':
        return render(request, 'drug/DrugUseByBarCode.html', locals())
    elif request.method == 'POST':
        drugIdList = eval(request.POST.get("drugId"))
        retrunData = ''
        userInfo = request.session['login_user']
        try:
            re={"terminal":'',"result":[]}
            for drugId in drugIdList:
                drugEntity = BllMedicament().findEntity(EntityMedicament.MedicamentId == drugId)
                client_obj = BllClient().findEntity(drugEntity.ClientId)
                # if (drugEntity.Status != DrugStatus.Normal and drugEntity.Status != DrugStatus.Empty and drugEntity.Place !=''):
                #     continue
                # elif (drugEntity.Status == DrugStatus.Empty and drugEntity.Place !=''):
                #     continue

                if drugEntity.Place !='':
                    try:
                        customerId = drugEntity.CustomerId
                        clientId = drugEntity.ClientId
                        goodDrug = BllMedicament().getDrugNearExpired(drugEntity.VarietyId, customerId)
                        drugEntity.ByUserDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        drugEntity.ByUserId = userInfo.get('UserId')
                        drugEntity.ByUserName = userInfo.get('RealName')
                        drugEntity.Status = DrugStatus.Out
                        BllMedicament().drugUse(drugEntity, BllClient().findEntity(clientId),
                                                BllUser().findEntity(userInfo.get('UserId')))
                        re["result"].append({"Name":drugEntity.Name,"Place":drugEntity.Place,"EnglishName":drugEntity.EnglishName,"CASNumber":drugEntity.CASNumber,"BarCode":drugEntity.BarCode,"Remain":drugEntity.Remain})
                    except Exception as e:
                        print(e)
            if re["result"]:
                AccuLockTcpServer.Data = {"terminal": client_obj.ClientName, "mes": 'lighton' + '~'.join([i["Place"] for i in re["result"]])}

                print('领用亮灯:', 'lighton' + "~".join([i["Place"] for i in re["result"]]))
                re["terminal"] =client_obj.ClientName
                retrunData = Utils.resultData(0, '试剂领用成功！',re)
            else:
                retrunData = Utils.resultData(1, '试剂领用失败！', re)

        except Exception as e:
            print(e)
            retrunData = Utils.resultData(1, str(e))
        return JsonResponse(retrunData)


# 试剂归还处理视图
@csrf_exempt
def drugReturnView(request):
    if request.method == 'GET':
        return render(request, 'drug/DrugReturnByBarCode.html', locals())
    elif request.method == 'POST':
        drugIdList = eval(request.POST.get("drugId"))
        Place = request.POST.get("Place")
        retrunData = ''
        userInfo = request.session['login_user']
        if drugIdList:
            drugEntity = BllMedicament().findEntity(EntityMedicament.MedicamentId == drugIdList[0])
            client_obj = BllClient().findEntity(drugEntity.ClientId)
            null_place = BllMedicament().get_boxlist(drugEntity.ClientId, type='back', num=len(drugIdList))
            if null_place == False:
                retrunData = Utils.resultData(1, '柜子余位不足！', data={"terminal":client_obj.ClientName,"result":[]})
                return JsonResponse(retrunData)
        try:
            re={"terminal":'',"result":[]}
            for drugId in drugIdList:
                drugEntity = BllMedicament().findEntity(EntityMedicament.MedicamentId == drugId)
                client_obj = BllClient().findEntity(drugEntity.ClientId)
                if (drugEntity is None):
                    retrunData = Utils.resultData(1, '药剂条码无效！')
                elif (drugEntity.Status != DrugStatus.Out):
                    retrunData = Utils.resultData(1, '此药剂未被领用！')
                else:
                    try:
                        customerId = drugEntity.CustomerId
                        clientId = drugEntity.ClientId
                        drugEntity.Status = DrugStatus.Normal
                        if Place:
                            drugEntity.Place = Place
                        BllMedicament().drugReturn(drugEntity, BllClient().findEntity(clientId),
                                                   BllUser().findEntity(userInfo.get('UserId')))
                        re["result"].append(
                            {"Name": drugEntity.Name, "Place": drugEntity.Place, "EnglishName": drugEntity.EnglishName,
                             "CASNumber": drugEntity.CASNumber, "BarCode": drugEntity.BarCode,
                             "Remain": drugEntity.Remain})
                    except Exception as e:
                        print(e)

            null_place = BllMedicament().get_boxlist(clientId, type='back',num =len(re["result"]))
            if null_place != False:
                for i in range(len(null_place)):
                    re["result"][i]["Place"] =null_place[i]
                AccuLockTcpServer.Data = {"terminal": client_obj.ClientName, "mes": 'lighton' + '~'.join(null_place)}
                print('归还亮灯:', 'lighton' + "~".join(null_place))
                re["terminal"] = client_obj.ClientName
                retrunData = Utils.resultData(0, '试剂归还成功！',data=re)
            else:
                retrunData = Utils.resultData(1, '柜子已满！', data=re)

        except Exception as e:
            print(e)
            retrunData = Utils.resultData(1, str(e))
        return JsonResponse(retrunData)


###########################
# 试剂入库iframe 页面返回视图
def DrugPutInByBarCode(request, template_id):
    # template_id = request.GET.get("template_id","none")
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
    return render(request, 'drug/DrugPutInByBarCode.html', locals())
