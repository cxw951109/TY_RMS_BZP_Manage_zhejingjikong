import json
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Business.BllClientVeision import BllClientVersion
from Lib.Utils import Utils
from DataEntity.EntityClientVersion import EntityClientVersion


# 获取版本管理首页
def index(request):
    search_word = request.GET.get('searchValue')
    return render(request, 'version/index.html', locals())


# 获取终端版本信息
def get_version_list_json(request):
    if request.method == 'GET':
        search_word = request.GET.get('searchValue')
        # 如果有值则代表搜索
        version_list = BllClientVersion().get_search_list(search_word)
        version_list = Utils.resultAlchemyData(version_list)
        return JsonResponse({'data': json.loads(version_list)})


# 新增版本信息
def add_version(request):
    if request.method == 'GET':
        version_id = request.GET.get('version_id')
        if not version_id:
            return render(request, 'version/add_version.html', locals())
        version_obj = BllClientVersion().findEntity(version_id)
        return render(request, 'version/add_version.html', locals())


# 保存版本信息
def save_version(request):
    version_id = request.POST.get('VersionId')
    version_code = request.POST.get('VersionCode')
    version_name = request.POST.get('VersionName')
    down_link = request.POST.get('DownLink')
    version_info = request.POST.get('VersionInfo')
    version_code_obj = BllClientVersion().findEntity(EntityClientVersion.VersionCode == version_code)
    if not version_id:
        # 获取当前登录用户
        if version_code_obj:
            return JsonResponse(Utils.resultData(0, '该版本号已存在，请重新输入!'))
        user = request.session['login_user']
        version_obj = EntityClientVersion(VersionId=str(Utils.UUID()), VersionName=version_name,
                                          VersionCode=version_code, DownLink=down_link, VersionInfo=version_info,
                                          CreateDate=datetime.now(), CreateUserId=user['UserId'],
                                          CreateUserName=user['RealName'], IsAdd=1)
        bool_ = BllClientVersion().insert(version_obj)
        if bool_:
            return JsonResponse(Utils.resultData(1, '新增成功！'))
        else:
            return JsonResponse(Utils.resultData(0, '新增失败, 数据异常！'))

    version_obj = BllClientVersion().findEntity(version_id)
    if not version_code_obj or version_code_obj.VersionCode == version_obj.VersionCode:
        version_obj.VersionCode = version_code
        version_obj.VersionName = version_name
        version_obj.DownLink = down_link
        version_obj.VersionInfo = version_info
        bool_ = BllClientVersion().update(version_obj)
        if bool_:
            return JsonResponse(Utils.resultData(1, '修改成功！'))
        else:
            return JsonResponse(Utils.resultData(0, '新增失败, 数据异常！'))
    else:
        return JsonResponse(Utils.resultData(0, '该版本号已存在，请重新输入!'))


# 删除指定的版本
@csrf_exempt
def delete_version(request):
    version_id = request.POST.get('VersionId')
    if version_id:
        BllClientVersion().delete(EntityClientVersion.VersionId==version_id)
        return JsonResponse(Utils.resultData(1, '删除成功'))
    else:
        return JsonResponse(Utils.resultData(0, '删除失败'))
