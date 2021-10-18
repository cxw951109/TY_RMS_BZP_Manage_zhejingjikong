from django.conf.urls import url

from . import views

app_name = 'warning'

urlpatterns = [
    # 预警列表首页
    url(r'index/.*?', views.index, name='index'),
    # 获取预警Json数据
    url(r'getWarningListJson/', views.getWarningListJson, name='getWarningListJson'),
    # 查看预警管理详情
    url(r'form/.*$', views.form, name='form'),
    # 保存预警已解决处理路由
    url(r'solveWarning', views.solveWarning, name='solveWarning'),
    #  每200毫秒请求一次预警路由信息 获取预警数量
    url(r'warning_numbers', views.warning_numbers, name='warning_numbers'),


]
