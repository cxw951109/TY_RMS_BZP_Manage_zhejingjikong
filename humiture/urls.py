from django.conf.urls import url

from . import views

app_name = 'humiture'

urlpatterns = [
    # 获取温湿度数据页面
    url(r'^index/$', views.index, name='index'),
    # 获取温湿度Json数据
    url(r'^getHumitureListJson/$', views.getHumitureListJson, name='getHumitureListJson'),
    # 获取温湿度Json数据
    url(r'^getHumitureListJson1/$', views.getHumitureListJson1, name='getHumitureListJson1'),
    # 获取温湿度echarts展示数据
    url(r'^getHumitureStatisticsJson/.*$', views.getHumitureStatisticsJson, name='getHumitureStatisticsJson'),
    # 导出温湿度记录
    url(r'^exportHumitureData/.*$', views.exportHumitureData, name='exportHumitureData'),
    # 导出温湿度记录
    url(r'^exportHumitureData1/.*$', views.exportHumitureData1, name='exportHumitureData1'),
]