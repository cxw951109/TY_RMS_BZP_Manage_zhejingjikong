from django.conf.urls import url

from . import views

app_name = 'stockTaking'

urlpatterns = [
    # 获取库存盘点页面
    url(r'^index/$', views.index, name='index'),
    # 校验库存路由
    url(r'^checkStock/$', views.checkStock, name='checkStock'),
    # 获取校验库存页面路由
    url(r'^resultPage/$', views.resultPage, name='resultPage'),
    # 获取前段传入的数据然后返回,datatable
    url(r'^getResultListJson/$', views.getResultListJson, name='getResultListJson'),
    # 查看指定类别的流转记录
    url(r'^stockingRecord/$', views.stockingRecord, name='stockingRecord'),
]
