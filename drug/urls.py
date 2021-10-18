from django.conf.urls import url

from . import views

app_name = 'drug'

urlpatterns = [

    # 删除试剂处理路由
    url(r'deleteDrug/$', views.deleteDrug, name='deleteDrug'),
    # 获取扫码查询的数据
    url(r'GetDrugJson/$', views.GetDrugJson, name='GetDrugJson'),
    # 获取扫码查询信息并且称重
    url(r'GetDrugJsonAndWeight/$', views.GetDrugJsonAndWeight, name='GetDrugJsonAndWeight'),
    # 试剂类别请求路由
    url(r'drugTypeIndex/$', views.drugTypeIndex, name='drugTypeIndex'),
    # 获得试剂类别的JSON数据
    url(r'getDrugTypeListJson/$', views.getDrugTypeListJson, name='getDrugTypeListJson'),
    # 新增试剂类别
    url(r'createDrugType/$', views.createDrugType, name='createDrugType'),
    # 修改试剂类别
    url(r'(?P<varietyId>(\w{8}-\w{4}-\w{4}-\w{4}-\w{12}))/drugEditorTypeForm/$', views.drugEditorTypeForm, name='drugEditorTypeForm'),
    url(r'deleteDrugType/$', views.deleteDrugType, name='deleteDrugType'),
    #返回一维条码试剂入库iframe
    url(r'(?P<template_id>(\w{8}-\w{4}-\w{4}-\w{4}-\w{12}))/DrugPutInByBarCode/$', views.DrugPutInByBarCode, name='DrugPutInByBarCode'),
    # url(r'DrugPutInByBarCode/$', views.DrugPutInByBarCode, name='DrugPutInByBarCode'),
    # url(r'^(?P<template_id>(\w{8}-\w{4}-\w{4}-\w{4}-\w{12}))/RFIDStorage/$', views.RFIDStorage, name='RFIDStorage'),
    # 试剂归还路由处理
    url(r'drug_weigh/$', views.drug_weigh, name='drug_weigh'),
    # 天平去皮路由处理
    url(r'balance_tare/$', views.balance_tare, name='balance_tare'),
    # 获取指定试剂归还信息
    url(r'GetDrugInfo/$', views.GetDrugInfo, name='GetDrugInfo'),
    # 实现socket通讯
    url(r'drug_socket/$', views.drug_socket, name='drug_socket'),
    # 试剂禁止使用用户
    url(r'disabled_user/$', views.disabled_user, name='disabled_user'),
    # 保存禁用用户
    url(r'saveDisabledUser/$', views.saveDisabledUser, name='saveDisabledUser'),

    # 设置试剂空瓶
    url(r'setDrugEmpty/$', views.setDrugEmpty, name='setDrugEmpty'),
    # 设置试剂图片
    url(r'setDrugImageUrl/$', views.setDrugImageUrl, name='setDrugImageUrl'),



    #试剂入库视图
    url(r'drugPutInView/$', views.drugPutInView, name='drugPutInView'),
    #试剂领用视图
    url(r'^drugUseView/$', views.drugUseView, name='drugUseView'),
    #试剂归还视图
    url(r'^drugReturnView/$', views.drugReturnView, name='drugReturnView'),
    #获取待归还试剂
    url(r'^getWaitRetrunDrugList/$', views.getWaitRetrunDrugList, name='getWaitRetrunDrugList'),

    # 查询危险品
    url(r"^danger/$", views.danger, name='danger'),
]
# \w{8}-\w{4}-\w{4}-\w{4}-\w{12}


