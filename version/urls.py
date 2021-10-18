from django.conf.urls import url

from . import views

app_name = 'version'

urlpatterns = [

    url(r'index/$', views.index, name='index'),
    # 获取所有的版本信息
    url(r'get_version_list_json/$', views.get_version_list_json, name='get_version_list_json'),
    # 新增版本信息
    url(r'add_version/.*?$', views.add_version, name='add_version'),
    # 保存新增或修改版本信息
    url(r'save_version/$', views.save_version, name='save_version'),
    # 删除版本信息
    url(r'delete_version/$', views.delete_version, name='delete_version'),

]
