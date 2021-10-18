from django.conf.urls import url

from . import views

app_name = 'approve'

urlpatterns = [

    # 审批设置列表页面
    url(r'^setIndex/$', views.setIndex, name='setIndex'),
    # 我发起的页面
    url(r'^mySend/$', views.mySend, name='mySend'),
    # 待我审批页面
    url(r'^myReceive/$', views.myReceive, name='myReceive'),

    # 审批表单页面
    url(r'^approveForm/$', views.approveForm, name='approveForm'),
    # 查看审批页面
    url(r'^approveView/$', views.approveView, name='approveView'),
    # 审批设置表单页面
    url(r'^setForm/$', views.setForm, name='setForm'),


    # 获取我申请的审批信息数据
    url(r'^getMySendApproveInfoListJson/$', views.getMySendApproveInfoListJson, name='getMySendApproveInfoListJson'),
    # 获取待我审批的审批信息数据
    url(r'^getMyReceiveApproveInfoListJson/$', views.getMyReceiveApproveInfoListJson, name='getMyReceiveApproveInfoListJson'),
    # 获取审批类型数据列表
    url(r'^getApproveTypeListJson/$', views.getApproveTypeListJson, name='getApproveTypeListJson'),


    # 保存审批类型数据
    url(r'^saveApproveTypeData/$', views.saveApproveTypeData, name='saveApproveTypeData'),
    # 提交审批决定
    url(r'^summitApproveDecide/$', views.summitApproveDecide, name='summitApproveDecide'),
    # 删除审批类型数据
    url(r'^deleteApproveType/$', views.deleteApproveType, name='deleteApproveType'),

]