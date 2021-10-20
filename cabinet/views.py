from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Business.BllClient import *
from Business.BllClientUser import *
from Business.BllClientCellUser import *
from Business.BllUser import *
from Business.BllMedicament import *
from DataEntity.EntityClient import *
from DataEntity.EntityClientCellUser import *
from Lib.RFIDNew import RFIDNew
from Lib.Relay import Relay
from Lib.Utils import *
# from Lib.RelayControl import RelayControl
from TY_RMS_Multiple_Manage.AccuLockTcpServer import *

try:
    RFID_object = RFIDNew()
except Exception as e:
    print(e, '1111111 RFID 通讯失败...')
try:
    relay_object = Relay()
except Exception as e:
    print(e, '继电器 通讯失败...')

data_relay = {"1_6": 1, "2_6": 2, "3_6": 3, "4_6": 4, "5_6": 5, "1_5": 6, "2_5": 7, "3_5": 8, "4_5": 9, "5_5": 10,
              "1_4": 11, "2_4": 12, "3_4": 13, "4_4": 14, "5_4": 15, "1_3": 16, "2_3": 17, "3_3": 18, "4_3": 19,
              "5_3": 20, "1_2": 21, "2_2": 22, "3_2": 23, "4_2": 24, "5_2": 25, "1_1": 26, "2_1": 27, "3_1": 28,
              "4_1": 29, "5_1": 30}


@require_http_methods(['GET'])
def getStayLabelJson(request):
    if request.method == 'GET':
        # data = RFID_object.get_stay_label()
        # print("标签-位置-------", data)
        data = [[1], [1]]
        return JsonResponse(Utils.resultData(1, "成功", data))


@require_http_methods(['GET'])
def controlSwitch(request):
    if request.method == 'GET':
        num = request.GET.get('num')
        if num is None:
            return JsonResponse(Utils.resultData(0, "参数有误", ""))
        if data_relay.get(num):
            num = data_relay.get(num)
        else:
            num = int(num)
        switch = request.GET.get('switch')
        print('参数:', num, switch)

        data = relay_object.control_switch(num, switch)
        # data = relay_object.control_switch(num, switch)
        if data == 'ok':
            return JsonResponse(Utils.resultData(1, data, ""))
        else:
            return JsonResponse(Utils.resultData(0, data, ""))

@require_http_methods(['GET'])
def index(request):
    if request.method == 'GET':
        try:
            user = request.session['login_user']
            account = user['Account']
        except Exception as e:
            print(e)
            account = ''
        searchValue = request.GET.get('searchValue', '')
        return render(request, 'cabinet/index.html', locals())


@require_http_methods(['GET'])
def mapIndex(request):
    if request.method == 'GET':
        try:
            user = request.session['login_user']
            account = user['Account']
        except Exception as e:
            print(e)
            account = ''
        searchValue = request.GET.get('searchValue', '')
        return render(request, 'cabinet/mapIndex.html', locals())


@require_http_methods(['GET'])
def getCabinetListJson(request):
    if request.method == 'GET':
        searchValue = request.GET.get('searchValue', '')
        if not searchValue:
            client_list = BllClient().findList().all()
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(client_list))})
        else:
            client_list = BllClient().like_ClientId_or_Name(searchValue)
            return JsonResponse({'data': json.loads(Utils.resultAlchemyData(client_list))})

@require_http_methods(['GET'])
def getSelectClientListJson(request):
    if request.method == 'GET':
        ClientUseCode = request.GET.get('type', '')
        if ClientUseCode:
            client_list = BllClient().getSelectClient(ClientUseCode)
            print(ClientUseCode, "1111111111111")
            return JsonResponse(client_list, safe=False)
        else:
            return JsonResponse([], safe=False)



# 更改用户状态 锁定/解锁药柜
@require_http_methods(['POST'])
@csrf_exempt
def lockCabinet(request):
    try:
        if request.method == 'POST':
            clientId = request.POST.get('clientId', '')
            if clientId:
                client_obj = BllClient().findEntity(clientId)
                if client_obj.IsEnabled == 1:
                    client_obj.IsEnabled = 0
                else:
                    client_obj.IsEnabled = 1
                BllClient().update(client_obj)
                return JsonResponse(Utils.resultData('1', '成功'))
            else:
                return JsonResponse(Utils.resultData('0', '请选中客户端Id'))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', e))

# 清空药柜数据
@require_http_methods(['POST'])
@csrf_exempt
def clearCabinet(request):
    try:
        if request.method == 'POST':
            clientId = request.POST.get('clientId', '')
            if clientId:
                BllClient().executeNoParam('delete from RMS_Medicament where ClientId=\''+clientId+'\'')
                BllClient().executeNoParam('delete from RMS_MedicamentRecord where ClientId=\''+clientId+'\'')
                BllClient().executeNoParam('delete from RMS_HumitureRecord where ClientId=\''+clientId+'\'')
                BllClient().executeNoParam('delete from RMS_MedicamentTemplate where ClientId=\''+clientId+'\'')
                return JsonResponse(Utils.resultData('1', '成功'))
            else:
                return JsonResponse(Utils.resultData('0', '请选中客户端Id'))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', e))

# 清空所有药柜数据
@require_http_methods(['POST'])
@csrf_exempt
def clearAllCabinet(request):
    try:
        if request.method == 'POST':
            BllClient().executeNoParam('delete from RMS_MedicamentVariety ')
            BllClient().executeNoParam('delete from RMS_Medicament ')
            BllClient().executeNoParam('delete from RMS_MedicamentRecord ')
            BllClient().executeNoParam('delete from RMS_Log ')
            BllClient().executeNoParam('delete from RMS_Warning ')
            BllClient().executeNoParam('delete from RMS_HumitureRecord ')
            BllClient().executeNoParam('delete from RMS_MedicamentTemplate ')
            return JsonResponse(Utils.resultData('1', '成功'))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', e))

# 删除药柜
@require_http_methods(['POST'])
@csrf_exempt
def deleteCabinet(request):
    try:
        if request.method == 'POST':
            clientId = request.POST.get('clientId', '')
            if clientId:
                BllClient().executeNoParam('delete from RMS_Medicament where ClientId=\''+clientId+'\'')
                BllClient().executeNoParam('delete from RMS_MedicamentRecord where ClientId=\''+clientId+'\'')
                BllClient().executeNoParam('delete from RMS_HumitureRecord where ClientId=\''+clientId+'\'')
                BllClient().executeNoParam('delete from RMS_MedicamentTemplate where ClientId=\''+clientId+'\'')

                BllClient().executeNoParam('delete from RMS_Client where ClientId=\''+clientId+'\'')
                return JsonResponse(Utils.resultData('1', '成功'))
            else:
                return JsonResponse(Utils.resultData('0', '请选中客户端Id'))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', e))


# 分配柜子给用户
@require_http_methods(['GET'])
def powerForm(request):
    if request.method == 'GET':

        ClientId = request.GET.get('clientId', '')
        if ClientId:
            user_list = BllUser().findList().all()
            client_user_obj_list = BllClientUser().findList(EntityClientUser.ClientId == ClientId).all()
            client_list = []
            if client_user_obj_list:
                for client_user_obj in client_user_obj_list:
                    client_list.append(client_user_obj.UserId)
            ClientId = ClientId
            return render(request, 'cabinet/powerForm.html', locals())

# 分配柜子格子权限给用户
@require_http_methods(['GET'])
def cellPowerForm(request):
    if request.method == 'GET':

        ClientId = request.GET.get('clientId', '')
        if ClientId:
            user_list = BllUser().findList().all()
            client_user_obj_list = BllClientUser().findList(EntityClientUser.ClientId == ClientId).all()
            client_list = []
            if client_user_obj_list:
                for client_user_obj in client_user_obj_list:
                    client_list.append(client_user_obj.UserId)
            ClientId = ClientId
            return render(request, 'cabinet/cellPowerForm.html', locals())


# 保存抽屉用户使用权限
@require_http_methods(['POST'])
@csrf_exempt
def saveCellPowerData(request):
    if request.method == 'POST':
        ClientId = request.POST.get('clientId', '')
        ClientCellCode = request.POST.get('clientCellCode', '')
        powerValue = request.POST.get('powerValue', '').split(',')
        user_number = 0
        if ClientId and ClientCellCode:
            BllClientCellUser().delete(and_(EntityClientCellUser.ClientId == ClientId,EntityClientCellUser.ClientCellCode==ClientCellCode))
            for user_id in powerValue:
                # client_user_obj = BllClientCellUser().findEntity(and_(EntityClientCellUser.UserId == user_id,
                #                                                   EntityClientCellUser.ClientId == ClientId))
                # if client_user_obj:
                #     continue
                clientCellUser_obj = EntityClientCellUser(ClientCellId='',ClientCellCode=ClientCellCode,ClientId=ClientId,ClientCode='',UserId=user_id,Id=str(Utils.UUID()))
                BllClientCellUser().insert(clientCellUser_obj)
                user_number += 1
            return JsonResponse(Utils.resultData('1', '保存成功, 共添加了{}个使用用户'.format(user_number)))
        return JSON(Utils.resultData('0', '请选择客户端Id'))


# 保存用户权限
@require_http_methods(['POST'])
@csrf_exempt
def savePowerData(request):
    if request.method == 'POST':
        ClientId = request.POST.get('clientId', '')
        powerValue = request.POST.get('powerValue', '').split(',')
        user_number = 0
        if ClientId:
            BllClientUser().delete(EntityClientUser.ClientId == ClientId)
            for user_id in powerValue:
                client_user_obj = BllClientUser().findEntity(and_(EntityClientUser.UserId == user_id,
                                                                  EntityClientUser.ClientId == ClientId))
                if client_user_obj:
                    continue
                clientUser_obj = EntityClientUser(ClientId=ClientId, UserId=user_id, ClientUserId=str(Utils.UUID()))
                BllClientUser().insert(clientUser_obj)
                user_number += 1
            return JsonResponse(Utils.resultData('1', '保存成功, 共添加了{}个禁用用户'.format(user_number)))
        return JSON(Utils.resultData('0', '请选择客户端Id'))

# 获取格子权限
@require_http_methods(['GET'])
def getCabinetCellPowerListJson(request):
    if request.method == 'GET':
        ClientId = request.GET.get('clientId', '')
        ClientCellCode = request.GET.get('clientCellCode', '')
        user_list = []
        if(ClientId and ClientCellCode):
            client_user_obj_list = BllClientCellUser().findList(and_(EntityClientCellUser.ClientId == ClientId,EntityClientCellUser.ClientCellCode==ClientCellCode)).all()
            if client_user_obj_list:
                for client_user_obj in client_user_obj_list:
                    user_list.append(client_user_obj.UserId)
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(user_list))})


# 编辑药柜预警参数
@require_http_methods(['GET'])
def warningSetting(request):
    if request.method == 'GET':
        ClientId = request.GET.get('ClientId', '')
        client_obj = BllClient().findEntity(ClientId)
        return render(request, 'cabinet/warningSetting.html', locals())


# 保存修改的预警参数
@require_http_methods(['POST'])
@csrf_exempt
def saveWarningSetting(request):
    if request.method == 'POST':
        try:
            client_obj=None
            ClientId = request.POST['ClientId']
            ClientCode = request.POST['ClientCode']
            xhClient=BllClient().findEntity(EntityClient.ClientCode==ClientCode)
            if ClientId:
                # TemperatureMaxValue = request.POST['TemperatureMaxValue']
                # HumidityMaxValue = request.POST['HumidityMaxValue']
                # TemperatureMinValue = request.POST['TemperatureMinValue']
                # HumidityMinValue = request.POST['HumidityMinValue']
                # FilterShelfLifeWarningValue = request.POST['FilterShelfLifeWarningValue']
                client_obj = BllClient().findEntity(ClientId)
                if(xhClient is not None and xhClient.ClientId != client_obj.ClientId):
                    return JsonResponse(Utils.resultData('0', '此序号已存在！'))
                # client_obj.TemperatureMaxValue = TemperatureMaxValue
                # client_obj.TemperatureMinValue = TemperatureMinValue
                # client_obj.HumidityMaxValue = HumidityMaxValue
                # client_obj.HumidityMinValue = HumidityMinValue
            else:
                if(xhClient is not None):
                    return JsonResponse(Utils.resultData('0', '此序号已存在！'))
                client_obj=EntityClient()
                client_obj.ClientId=Utils.UUID()
                client_obj.IsEnabled=1
            client_obj.Place=request.POST['Place']
            client_obj.ContactPeopleName=request.POST['ContactPeopleName']
            client_obj.ClientCode=ClientCode
            client_obj.ClientName=ClientCode+'号终端'
            client_obj.ClientTitle=request.POST['ClientTitle']
            client_obj.ClientUseCode=request.POST['ClientUseCode']
            client_obj.ContactPhone=request.POST['ContactPhone']
            client_obj.Description=request.POST['Description']
            client_obj.FilterProductionDate=request.POST['FilterProductionDate']
            client_obj.FilterShelfLifeWarningValue = request.POST['FilterShelfLifeWarningValue']
            if ClientId:
                BllClient().update(client_obj)
            else:
                BllClient().insert(client_obj)
            return JsonResponse(Utils.resultData('1', '保存成功'))
        except:
            return JsonResponse(Utils.resultData('0', '数据异常，保存失败！'))

@require_http_methods(['GET'])
def openDoor(request):
    if request.method == 'GET':
        doorIndex = request.GET.get('doorIndex', '1')
        switch = request.GET.get('switch', '-1')
        # if(switch=='-1'):
        #     RelayControl.Case.openDoor(int(doorIndex))
        # elif(switch=='1'):
        #     RelayControl.Case.doorControl(int(doorIndex),True)
        # elif(switch=='0'):
        #     RelayControl.Case.doorControl(int(doorIndex),False)
        return JsonResponse(Utils.resultData('1', '开门成功!'))

@require_http_methods(['GET'])
def getOpenDoorList(request):
    if request.method == 'GET':
        openDoorList = []
        return JsonResponse(Utils.resultData('1', '获取成功!',openDoorList))




