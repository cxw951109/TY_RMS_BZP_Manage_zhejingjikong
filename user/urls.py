from django.conf.urls import url

from . import views

app_name = 'user'
urlpatterns = [
    # 用户页面
    url(r'^index/', views.index, name='index'),
    # 获取用户列表
    url(r'^getUserListJson/$', views.getUserListJson, name='getUserListJson'),
    # 获取角色列表
    url(r'^getRoleListJson/$', views.getRoleListJson, name='getRoleListJson'),
    # 用户表单页面

    url(r'^form/.*?$', views.user_form, name='form'),
    # 用户权限表单页面
    url(r'^importForm/$', views.user_importForm, name='importForm'),
    # 保存用户新增或修改数据
    url(r'^saveUserData/$', views.saveUserData, name='saveUserData'),
    # 删除用户操作
    url(r'^deleteUser/$', views.deleteUser, name='deleteUser'),
    # 锁定用户
    url(r'^lockUser/$', views.lockUser, name='lockUser'),
    # 获取用户功能权限页面
    url(r'^(?P<user_id>(\w{8}-\w{4}-\w{4}-\w{4}-\w{12}))/powerForm/$', views.powerForm, name='powerForm'),
    # 修改用户功能数据
    url(r'^savePowerData/$', views.savePowerData, name='savePowerData'),
    # 用户点击打印条码处理路由
    url(r'^printer_user_code/$', views.printer_user_code, name='printer_user_code'),

    # 用户角色列表页面
    url(r'^roleIndex/', views.roleIndex, name='roleIndex'),
    # 用户角色表单页面
    url(r'^roleForm/', views.roleForm, name='roleForm'),
    # 保存角色数据
    url(r'^saveRoleData/$', views.saveRoleData, name='saveRoleData'),
    # 删除角色操作
    url(r'^deleteRole/$', views.deleteRole, name='deleteRole'),

]
