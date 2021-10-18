import json
import datetime

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http import JsonResponse

from Business.BllUser import *
from Business.BllUserFace import *
from Business.BllModule import *
from Business.BllModuleRelation import *
from Business.BllRole import *
from DataEntity.EntityUser import *
from DataEntity.EntityUserFace import *
from DataEntity.EntityRole import *
from DataEntity.EntityModule import *
from Lib.Model import *
from Lib.create_barcode import CreateBarcode
from Lib.AlchemyJsonEncoder import *

# 获取用户列表Json数据
@require_http_methods(['GET'])
def getUserListJson(request):
    if request.method == 'GET':
        searchValue = request.GET.get('searchValue', '')
        curPage = int(request.GET.get('page', '1'))
        pageSize = int(request.GET.get('limit', '10'))
        pageParam = PageParam(curPage,pageSize)
        data = BllUser().getUserList("1002437b-debf-46d6-b186-3e16bcf0cc0f",pageParam,searchValue)
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':pageParam.totalRecords})

# 获取角色列表Json数据
@require_http_methods(['GET'])
def getRoleListJson(request):
    if request.method == 'GET':
        SQL="""
         SELECT r.*, group_concat(CASE WHEN b.ModuleType='1' THEN b.ModuleName END) AS ClientModuleList , 
         group_concat(CASE WHEN b.ModuleType='2' THEN b.ModuleName END) AS SysModuleList  
         FROM rms_role r LEFT JOIN `RMS_ModuleRelation` as a on r.RoleId = a.ObjectId AND a.ObjectType = 1
         LEFT JOIN RMS_Module as b on a.ModuleId = b.ModuleId GROUP BY r.RoleId Order BY SortIndex DESC
        """
        module_list = BllRole().execute(SQL).fetchall()
        module_list = Utils.mysqlTable2Model(module_list)
        data = module_list
        return JsonResponse({'data': json.loads(Utils.resultAlchemyData(data)),'code' : 0,'msg':'','count':10000})


@require_http_methods(['GET'])
def index(request):
    if request.method == 'GET':
        searchValue = request.GET.get('searchValue', '')
        all_role_json_list=BllRole().getRoleList()
        return render(request, 'user/index.html', locals())

@require_http_methods(['GET'])
def roleIndex(request):
    if request.method == 'GET':
        searchValue = request.GET.get('searchValue', '')
        all_moudule_json_list= json.dumps(BllModule().findList().order_by('SortIndex').all(),cls=AlchemyEncoder)
        return render(request, 'user/roleIndex.html', locals())


@require_http_methods(['GET'])
def user_importForm(request):
    if request.method == 'GET':
        return render(request, 'user/importForm.html', locals())


# 新增或修改用户
@require_http_methods(['GET'])
def user_form(request):
    if request.method == 'GET':
        try:
            # 如何user_id有值那就代表是修改
            user_id = request.GET.get("user_id",'')
            user = BllUser().findEntity(user_id)
            all_role_json_list=BllRole().getRoleList()
            return render(request, 'user/form.html', locals())
        except:
            pass
        return render(request, 'user/form.html', locals())

# 新增或修改角色
@require_http_methods(['GET'])
def roleForm(request):
    if request.method == 'GET':
        try:
            # 如何user_id有值那就代表是修改
            role_id = request.GET.get('role_id','')
            role = BllRole().findEntity(role_id)
            SQL = """
            SELECT c.ModuleId, c.ModuleCode, c.SortIndex, c.ModuleName,c.ModuleType from(
            SELECT a.ModuleId, b.ModuleCode, b.SortIndex, b.ModuleName,b.ModuleType FROM `RMS_ModuleRelation` as a
                LEFT JOIN RMS_Module as b on a.ModuleId = b.ModuleId  WHERE ObjectId = :role_id and ObjectType = 1) 
                as c ORDER BY c.SortIndex asc;
            """
            module_relation_obj_list = BllUser().execute(SQL, {'role_id': role_id}).fetchall()
            module_relation_obj_list = Utils.mysqlTable2Model(module_relation_obj_list)
            # # 获取UserId为当前选中用户Id的模型关系列表
            # module_relation_obj_list = BllModuleRelation().findList(and_(EntityModuleRelation.ObjectId == UserId,
            #                                                              EntityModuleRelation.ObjectType == 2))
            # 将获取到的功能数据列表按SortIndex排序
            all_moudule_list= BllModule().findList().order_by('SortIndex').all()
            sys_object_id_list = [x['ModuleId'] for x in module_relation_obj_list if x['ModuleType']=='2']
            # 用列表推导式生成一个ModuleId列表
            sys_function_model_obj_list = [x for x in all_moudule_list if x.ModuleType=='2']


            client_object_id_list = [x['ModuleId'] for x in module_relation_obj_list if x['ModuleType']=='1']
            # 用列表推导式生成一个ModuleId列表
            client_function_model_obj_list = [x for x in all_moudule_list if x.ModuleType=='1']
            return render(request, 'user/roleForm.html', locals())
        except Exception as e:
            print(str(e))
        return render(request, 'user/roleForm.html', locals())


# 保存用户新增或修改数据
@require_http_methods(['POST'])
@csrf_exempt
def saveUserData(request):
    if request.method == 'POST':
        UserId = request.POST['UserId']
        UserCode = request.POST['UserCode']
        BarCode = request.POST['BarCode']
        RealName = request.POST['realName']
        RoleId = request.POST['RoleId']
        RoleName=BllRole().findEntity(RoleId).RoleName
        Birthday = request.POST.get("Birthday",'') or datetime.datetime.now().strftime('%Y-%m-%d')
        Sex = request.POST['Sex']
        QQ = request.POST['QQ']
        Email = request.POST['Email']
        Mobile = request.POST['Mobile']
        SignUrl = request.POST.get('SignUrl','')
        Description = request.POST.get('Description','')
        IsEnabled = request.POST.get("IsEnabled",0)
        CreateDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not UserId:
            user = BllUser().findEntity(EntityUser.UserCode == UserCode)
            if user is None:
                UserId = str(Utils.UUID())
                user = EntityUser(UserId=UserId, BarCode=BarCode, RoleName=RoleName, RealName=RealName, UserCode=UserCode,RoleId=RoleId,
                                    Birthday=Birthday, Sex=Sex, QQ=QQ, Email=Email, Mobile=Mobile, SignUrl=SignUrl,Description=Description, IsEnabled=IsEnabled, Account=UserCode,
                                    CreateDate=CreateDate, Password=(Utils.MD5('000000')).upper(),
                                    CustomerId='1002437b-debf-46d6-b186-3e16bcf0cc0f')
                BllUser().insert(user)
                return JsonResponse(Utils.resultData('1', '保存成功', ''))
            else:
                return JsonResponse(Utils.resultData('0', '用户工号必须唯一, 该工号已存在', ''))
        else:
            user = BllUser().findEntity(UserId)
            user_ = BllUser().findEntity(EntityUser.UserCode == UserCode)

            if user_ is None or user.UserCode == user_.UserCode:
                user__ = BllUser().findEntity(EntityUser.BarCode == BarCode)
                if True:
                    user.RoleId = RoleId
                    user.RealName = RealName
                    user.RoleName = RoleName
                    user.UserCode = UserCode
                    user.Account = UserCode
                    user.BarCode = BarCode
                    user.Birthday = Birthday
                    user.Sex = Sex
                    user.Email = Email
                    user.QQ = QQ
                    user.Mobile = Mobile
                    user.SignUrl = SignUrl
                    user.Description = Description
                    user.IsEnabled = IsEnabled
                    BllUser().update(user)
                    return JsonResponse(Utils.resultData('1', '修改成功', ''))
                else:
                    return JsonResponse(Utils.resultData('0', '用户编号必须唯一, 该编号已存在', ''))
            else:
                return JsonResponse(Utils.resultData('0', '用户工号必须唯一, 该工号已存在', ''))


# 删除用户
@require_http_methods(['POST'])
@csrf_exempt
def deleteUser(request):
    try:
        if request.method == 'POST':
            deleteIds = request.POST.get("deleteIds",'')
            deleteIds=deleteIds.split(',')
            for userId in deleteIds:
                BllUser().delete(EntityUser.UserId==userId)
                BllUserFace().delete(EntityUserFace.UserId==userId)
            return JsonResponse(Utils.resultData('1', '删除成功', ''))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))

# 删除角色
@require_http_methods(['POST'])
@csrf_exempt
def deleteRole(request):
    try:
        if request.method == 'POST':
            deleteIds = request.POST.get("deleteIds",'')
            deleteIds=deleteIds.split(',')
            for roleId in deleteIds:
                BllModuleRelation().delete(EntityModuleRelation.ObjectId == roleId)
                BllRole().delete(EntityRole.RoleId==roleId)
            return JsonResponse(Utils.resultData('1', '删除成功', ''))
    except Exception as e:
        return JsonResponse(Utils.resultData('0', str(e), ''))


# 锁定用户
@require_http_methods(['POST'])
@csrf_exempt
def lockUser(request):
    if request.method == 'POST':
        userId = request.POST['userId']
        user = BllUser().findEntity(userId)
        if user.IsEnabled:
            user.IsEnabled = 0
            BllUser().update(user)
        else:
            user.IsEnabled = 1
            BllUser().update(user)
        return JsonResponse(Utils.resultData('1', '删除成功', ''))


# 获取用户功能数据
@require_http_methods(['GET'])
def powerForm(request, user_id):
    if request.method == 'GET':
        UserId = user_id
        user = BllUser().findEntity(user_id)
        role_id = user.RoleId
        SQL = """
        
        SELECT c.ModuleId, c.ModuleCode, c.SortIndex, c.ModuleName from(SELECT a.ModuleId, b.ModuleCode, 
        b.SortIndex, b.ModuleName FROM `RMS_ModuleRelation` as a LEFT JOIN RMS_Module as b on a.ModuleId = 
        b.ModuleId WHERE ObjectId = :user_id and ObjectType = 2 UNION
        SELECT a.ModuleId, b.ModuleCode, b.SortIndex, b.ModuleName FROM `RMS_ModuleRelation` as a
            LEFT JOIN RMS_Module as b on a.ModuleId = b.ModuleId  WHERE ObjectId = :role_id and ObjectType = 1) 
            as c ORDER BY c.SortIndex asc;
        """
        module_relation_obj_list = BllUser().execute(SQL, {'user_id': user_id, 'role_id': role_id}).fetchall()
        module_relation_obj_list = Utils.mysqlTable2Model(module_relation_obj_list)
        # # 获取UserId为当前选中用户Id的模型关系列表
        # module_relation_obj_list = BllModuleRelation().findList(and_(EntityModuleRelation.ObjectId == UserId,
        #                                                              EntityModuleRelation.ObjectType == 2))
        # 将获取到的功能数据列表按SortIndex排序
        function_model_obj_list = BllModule().findList().order_by('SortIndex')
        # 用列表推导式生成一个ModuleId列表
        object_id_list = [x['ModuleId'] for x in module_relation_obj_list]
        return render(request, 'user/powerForm.html', locals())


# 保存功能数据
@require_http_methods(['POST'])
@csrf_exempt
def savePowerData(request):
    if request.method == 'POST':
        UserId = request.POST['userId']
        powerValue = request.POST['powerValue']
        # 将存入的字符串格式以逗号分隔转换成列表
        powerValue = powerValue.split(',')
        BllModuleRelation().delete(EntityModuleRelation.ObjectId == UserId)
        for power in powerValue:
            entity_module = EntityModuleRelation(ModuleRelationId=str(Utils.UUID()), ObjectType=2, ObjectId=UserId, ModuleType=1, ModuleId=power)
            BllModuleRelation().insert(entity_module)
        return JsonResponse(Utils.resultData('1', ' 保存成功'))


# 保存用户角色
@require_http_methods(['POST'])
@csrf_exempt
def saveRoleData(request):
    if request.method == 'POST':
        RoleId = request.POST.get('RoleId')
        RoleCode = request.POST.get('RoleCode','')
        RoleName = request.POST.get('RoleName','')
        Description = request.POST.get('Description')
        SysPowerValue = request.POST.get('SysPowerValue')
        ClientPowerValue = request.POST.get('ClientPowerValue')
        
        # 根据RoleId是否有值判断是创建还是修改
        if not RoleId:
            role = BllRole().findEntity(or_(EntityRole.RoleCode == RoleCode,EntityRole.RoleName==RoleName))
            if role is None:
                RoleId = str(Utils.UUID())
                SQL = """SELECT max(SortIndex) as SortIndex FROM `rms_role`;"""
                role_max_obj = BllRole().execute(SQL).fetchone()
                role = EntityRole(RoleId=RoleId, RoleCode=RoleCode, RoleName=RoleName,Description=Description,
                                   RoleLevel=1,SortIndex=int(role_max_obj.SortIndex or '0')+1,IsEnabled=1,IsAdd=0)
                BllRole().insert(role)
            else:
                return JsonResponse(Utils.resultData('0', '角色代码或名称已存在', ''))
        else:
            role = BllRole().findEntity(RoleId)
            role_ = BllRole().findEntity(or_(EntityRole.RoleCode == RoleCode,EntityRole.RoleName==RoleName))
            if role_ is None or role.RoleId==role_.RoleId:
                role.RoleId = RoleId
                role.RoleName = RoleName
                role.RoleCode = RoleCode
                role.Description = Description
                BllRole().update(role)
            else:
                return JsonResponse(Utils.resultData('0', '角色代码或名称已存在', ''))
        # 将存入的字符串格式以逗号分隔转换成列表
        BllModuleRelation().delete(EntityModuleRelation.ObjectId == RoleId)
        if SysPowerValue:
            SysPowerList = SysPowerValue.split(',')
            for power in SysPowerList:
                entity_module = EntityModuleRelation(ModuleRelationId=str(Utils.UUID()), ObjectType=1, ObjectId=RoleId, ModuleType=2, ModuleId=power,CreateDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                BllModuleRelation().insert(entity_module)
        if ClientPowerValue:
            ClientPowerList = ClientPowerValue.split(',')
            for power in ClientPowerList:
                entity_module = EntityModuleRelation(ModuleRelationId=str(Utils.UUID()), ObjectType=1, ObjectId=RoleId, ModuleType=1, ModuleId=power,CreateDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                BllModuleRelation().insert(entity_module)
        return JsonResponse(Utils.resultData('1', ' 保存成功'))




# 用户点击打印条码  生成Code128 并调用打印机打印事件
def printer_user_code(request):
    try:
        if request.method == 'GET':
            barcode = request.GET.get('BarCode', '')

            if barcode:
                # 打印用户条码执行函数
                CreateBarcode().create_Code128_img(str(barcode))
                time.sleep(0.1)
                return JsonResponse(Utils.resultData('0', '打印成功！'))
        else:
            return JsonResponse(Utils.resultData('1', '用户条码未获取！'))
    except Exception as e:
        print(e)
        return JsonResponse(Utils.resultData(1, '打印失败，数据异常！'))
