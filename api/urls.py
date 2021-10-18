from django.conf.urls import url

from . import views

app_name = 'api'

urlpatterns = [

    # 获取试剂Json数据
    url(r'^getDrugList/$', views.getDrugList, name='getDrugList'),

    # 获取用户列表
    url(r'^getUserList/$', views.getUserList, name='getUserList'),


    # 获取用户流转记录
    url(r'^getDrugRecordList/$', views.getDrugRecordList, name='getDrugRecordList'),
]