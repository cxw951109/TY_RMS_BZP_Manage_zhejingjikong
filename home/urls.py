from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
    # 个人信息页面
    url(r'^myInfo/$', views.myInfo, name='myInfo'),
    # 保存用户个人信息
    url(r'^saveMyBaseInfo/$', views.saveMyBaseInfo, name='saveMyBaseInfo'),
    # 保存用户密码
    url(r'^saveMyPwd/$', views.saveMyPwd, name='saveMyPwd'),
    # 获取保存重置用户密码页面
    url(r'^(?P<user_id>(\w{8}-\w{4}-\w{4}-\w{4}-\w{12}))/saveUser/$', views.saveUser, name='saveMyPwd'),
    # 获取首页的近期预警列表
    url(r'^getWarningList/$', views.getWarningList, name='getWarningList'),
    # 获取入今日入库. 今日领用. 今日归还返回页面
    url(r'^homeDrugRecord/.*?$', views.homeDrugRecord, name='homeDrugRecord'),
    url(r'^homeDrugDetail/.*?$', views.homeDrugDetail, name='homeDrugDetail'),

    # 获取今日入库. 今日领用. 今日归还JSon数据
    url(r'^getRecordTypeDrugRecordListJson/$', views.getRecordTypeDrugRecordListJson,
        name='getRecordTypeDrugRecordListJson'),
    # 获取首页预警记录页面
    url(r'^homeWarningRecord/.*?$', views.homeWarningRecord, name='homeWarningRecord'),
    # 获取预警类型Json数据
    url(r'^homeWarningListJson/', views.homeWarningListJson, name='homeWarningListJson'),
    #获取库存中的详细记录页面
    url(r'^homeDescription/$', views.homeDescription, name='homeDescription'),
    #获取库存中的详细记录Json数据
    url(r'^homeDescriptionJson/$', views.homeDescriptionJson, name='homeDescriptionJson'),
    #获取试剂详情页面
    url(r'^homeMedicamentDescription/$', views.homeMedicamentDescription, name='homeMedicamentDescription'),
    #获取试剂详情页面json数据
    url(r'^homeMedicamentDescriptionJson/$', views.homeMedicamentDescriptionJson, name='homeMedicamentDescriptionJson'),


]