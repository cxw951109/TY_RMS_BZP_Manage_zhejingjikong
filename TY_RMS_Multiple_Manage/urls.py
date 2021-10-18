"""TY_RMS_Multiple URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'multiple'

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^main/', views.main, name='main'),
    url(r'^user/', include('user.urls')),
    url(r'^drug/', include('drug.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^log/', include('log.urls')),
    url(r'^warning/', include('warning.urls')),
    url(r'^humiture/', include('humiture.urls')),
    url(r'^cabinet/', include('cabinet.urls')),
    url(r'^dataReport/', include('dataReport.urls')),
    url(r'^drugTemplate/', include('drugTemplate.urls')),
    url(r'^stockTaking/', include('stockTaking.urls')),
    url(r'^version/', include('version.urls')),
    url(r'^approve/', include('approve.urls')),
    url(r'^standard/', include('standard.urls')),

    url(r'^keyCabinet/', include('keyCabinet.urls')),
    
    # 登录
    url(r'^account/login/$', views.account_login, name='account_login'),
    url(r'^account/barcode/$', views.account_barcode, name='account_barcode'),
    # 退出系统
    url(r'^account/logout/$', views.account_logout, name='account_logout'),
    # 试剂扫码查询
    url(r'^drug/scanBarCode/$', views.drug_scanBarCode, name='drug_scanBarCode'),
    # 试剂列表首页
    url(r'^drug/index/$', views.drug_index, name='drug_index'),
    # 编辑试剂表单页面
    url(r'^drug/form/$', views.drug_form, name='drug_form'),
    # 试剂表单页面
    url(r'^drug/drugTypeForm/$', views.drug_drugTypeForm, name='drug_drugTypeForm'),
    # 获取试剂类型列表json处理url
    url(r'^drug/GetDrugListJson/$', views.drug_GetDrugListJson, name='drug_GetDrugListJson'),
    # 获取试剂类型的JSON数据
    url(r'^drug/GetDrugTypeListJson/$', views.drug_GetDrugTypeListJson, name='drug_GetDrugTypeListJson'),
    # 试剂模板页面首页
    url(r'^drugTemplate/index/$', views.drugTemplate_index, name='drugTemplate_index'),
    # 新增试剂模板
    url(r'^drugTemplate/form/$', views.drugTemplate_form, name='drugTemplate_form'),
    # 修改试剂
    url(r'^drugTemplate/(?P<template_id>.*)/update_form/$', views.drugTemplate_update_form, name='drugTemplate_update_form'),
    # 新增单次模板条目
    url(r'^drugTemplate/itemForm/$', views.drugTemplate_itemForm, name='drugTemplate_itemForm'),
    # 新增模板视图路由
    url(r'^drugTemplate/SaveTemplateData/$', views.drugTemplate_saveTemplateData, name='drugTemplate_saveTemplateData'),
    # 获取访问入库模板JSON数据
    url(r'^drugTemplate/getTemplateListJson/$', views.drugTemplate_getTemplateListJson, name='drugTemplate_getTemplateListJson'),
    # 获取ClientId Json数据
    url(r'^drugTemplate/ClientListJson/$', views.drugTemplate_clientListJson, name='drugTemplate_clientListJson'),
    # 删除模板
    url(r'^drugTemplate/deleteTemplate/$', views.drugTemplate_deleteTemplate, name='drugTemplate_deleteTemplate'),
    # 日志列表首页
    url(r'^log/index/$', views.log_index, name='log_index'),
    #mxh_试剂详细信息统计
    url(r'dataReport/drug_GetDrugListJson/$',views.drug_GetDrugListJson,name='drug_GetDrugListJson'),
    # 首页试剂记录页面
    url(r'^home/(?P<drug_id>.*)/homeDrugRecord/$', views.home_homeDrugRecord, name='home_homeDrugRecord'),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'TY_RMS_Multiple_Manage.views.page_not_found'
