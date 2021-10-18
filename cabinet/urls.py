from django.conf.urls import url

from . import views

app_name = 'cabinet'

urlpatterns = [
    # 药柜列表首页
    url(r'^index/$', views.index, name='index'),

    # 库房示意
    url(r'^mapIndex/$', views.mapIndex, name='mapIndex'),

    # 获取终端Json数据
    url(r'^getCabinetListJson/$', views.getCabinetListJson, name='getCabinetListJson'),
    # 获取柜子抽屉权限Json数据
    url(r'^getCabinetCellPowerListJson/$', views.getCabinetCellPowerListJson, name='getCabinetCellPowerListJson'),
    # 获取柜子选择Json数据
    url(r'^getSelectClientListJson/$', views.getSelectClientListJson, name='getSelectClientListJson'),

    # 锁定或解除药柜
    url(r'^lockCabinet/$', views.lockCabinet, name='lockCabinet'),
    # 清空药柜数据
    url(r'^clearCabinet/$', views.clearCabinet, name='clearCabinet'),
    # 清空所有药柜数据
    url(r'^clearAllCabinet/$', views.clearAllCabinet, name='clearAllCabinet'),
    # 删除药柜
    url(r'^deleteCabinet/$', views.deleteCabinet, name='deleteCabinet'),
    # 给用户分配权限页面
    url(r'^powerForm/$', views.powerForm, name='powerForm'),
    # 给用户分配抽屉格子权限页面
    url(r'^cellPowerForm/$', views.cellPowerForm, name='cellPowerForm'),
    # 保存分配的用户权限
    url(r'^savePowerData/$', views.savePowerData, name='savePowerData'),
    # 保存分配的柜子格子权限
    url(r'^saveCellPowerData/$', views.saveCellPowerData, name='saveCellPowerData'),
    # 获取预警参数页面
    url(r'^warningSetting/.*$', views.warningSetting, name='warningSetting'),
    # 保存修改的预警参数
    url(r'^saveWarningSetting/.*$', views.saveWarningSetting, name='saveWarningSetting'),

    url(r'^openDoor/$', views.openDoor, name='openDoor'),

    url(r'^getOpenDoorList/$', views.getOpenDoorList, name='getOpenDoorList'),

    # 获取标签所在的位置
    url(r'^getStayLabelJson/$', views.getStayLabelJson, name='getStayLabelJson'),
    # 继电器开关
    url(r'^controlSwitch/$', views.controlSwitch, name='controlSwitch'),
]
