import threading
from dwebsocket.decorators import accept_websocket

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Business.BllMedicament import *
from Business.BllUser import *
from Business.BllUserMedicament import *
from DataEntity.EntityMedicamentVariety import *
from Lib.Balance import Balance
from Lib.RFIDDevice import RFIDDevice

try:
    RFID_cls = RFIDDevice()
except Exception as e:
    print(e, 'RFID 通讯失败...')


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
                    BllMedicament().update(medicamentVa_obj)

            BllMedicament().delete_drug(MedicamentId=MedicamentId, medicament_obj=medicament_obj)
            return JsonResponse(Utils.resultData('1', '删除成功', ''))
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
        data = BllMedicamentVariety().findEnglishOrChinseNameList(searchValue).order_by(desc(EntityMedicamentVariety.CreateDate)).all()
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
        # 根据VarietyId是否有值判断是创建新的试剂类别还是修改
        if not VarietyId:
            VarietyId = str(Utils.UUID())
            BllMedicamentVariety_obj = BllMedicamentVariety().findList(EntityMedicamentVariety.Name==Name, EntityMedicamentVariety.EnglishName==EnglishName).all()

            if not BllMedicamentVariety_obj:
                user = request.session['login_user']
                medicamentVariety = EntityMedicamentVariety(VarietyId=VarietyId, Name=Name, EnglishName=EnglishName,
                                                            CASNumber=CASNumber, Purity=Purity, Remark1=Remark1, EmptyCount=0,
                                                            UseCount=0, NormalCount=0, TotalCount=0, CreateUserId=user['UserId'],
                                                            CreateUserName=user['RealName'],
                                                            InventoryWarningValue=InventoryWarningValue, Remark2=Remark2,
                                                            ShelfLifeWarningValue=ShelfLifeWarningValue, Remark3=Remark3,
                                                            UseDaysWarningValue=UseDaysWarningValue,CustomerId=CustomerId,
                                                            IsSupervise=IsSupervise, CreateDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
            BllMedicamentVariety().update(medicamentVariety)
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
        BllMedicamentVariety().delete(EntityMedicamentVariety.VarietyId==varietyId)
        return  JsonResponse(Utils.resultData('1', '删除成功', ''))


# 获取扫码查询的数据
def GetDrugJson(request):
    drug_id = request.GET.get('drugId', '')
    if drug_id:
        medicament_obj = BllMedicament().findEntity(EntityMedicament.BarCode==drug_id)
        if medicament_obj:
            medicament_obj = Utils.resultAlchemyData(medicament_obj)
            return JsonResponse({'data': Utils.resultData(1, '获取成功', data=medicament_obj)})
        else:
            return JsonResponse({'data': Utils.resultData(0, '没有该编号')})
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
            drug_obj.Remain = remain  # 余量
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
                        return JsonResponse({'data': Utils.resultData(0, '数据异常，请检查串口是否连接！')})

                    a.write('#')
                    drug_margin = a.read()
                    if drug_margin:
                        if drug_margin and drug_margin != '关机':
                            drug_margin = drug_margin
                        elif drug_margin == '关机':
                            return JsonResponse({'data': Utils.resultData(0, '请检查天平是否开机!')})
                        else:
                            return JsonResponse({'data': Utils.resultData(0, '余量为负， 请校准天平！')})
                        return JsonResponse({'data': Utils.resultData(1, '获取成功', data=medicament_obj), 'drug_margin': drug_margin})

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
                                time.sleep(1)

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
                request.websocket.close()
                return
            except:
                return


# 试剂禁止使用用户
def disabled_user(request):
    if request.method == 'GET':
        barcode = request.GET.get('barcode', '')
        if barcode:
            drug_obj = BllMedicament().findEntity(EntityMedicament.BarCode == barcode)
            print(drug_obj, 888888888)
            user_list = BllUser().findList().all()
            BllUserMedicament_obj_list = BllUserMedicament().findList(EntityUserMedicament.DrugId == drug_obj.MedicamentId).all()
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
