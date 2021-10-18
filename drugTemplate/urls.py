from django.conf.urls import url

from . import views

app_name = 'drugTemplate'

urlpatterns = [
    # 自动搜索试剂处理路由
    url(r'^autoSearchDrugList/.*?', views.autoSearchDrugList, name='autoSearchDrugList'),
    # RFID试剂入库路由
    url(r'^(?P<template_id>(\w{8}-\w{4}-\w{4}-\w{4}-\w{12}))/RFIDStorage/$', views.RFIDStorage, name='RFIDStorage'),
    # RFID标签绑定模板
    url(r'^bind_template/$', views.bind_template, name='bind_template'),
    # 打印模板试剂条码
    url(r'^printer_drug_code/$', views.printer_drug_code, name='printer_drug_code'),

    #导入入库模板
    url(r'^exportPutInTemplate/$', views.exportPutInTemplate, name='exportPutInTemplate'),
]
