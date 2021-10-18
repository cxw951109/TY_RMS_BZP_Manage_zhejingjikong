from django.conf.urls import url

from . import views

app_name = 'log'

urlpatterns = [
    # 获取日志数据页面
    url(r'^index/$', views.index, name='index'),
    # 获取日志Json数据
    url(r'^getLogListJson/$', views.getLogListJson, name='getLogListJson'),
    # 导入日志数据处理路由
    url(r'^exportLogData/$', views.exportLogData, name='exportLogData'),
]