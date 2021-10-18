from django.conf.urls import url

from . import views

app_name = 'keyCabinet'

urlpatterns = [
    # 检材入库页面
    url(r'^materialStockIn/$', views.materialStockIn, name='materialStockIn'),
    # 添加检材页面
    url(r'^addMaterialForm/$', views.addMaterialForm, name='addMaterialForm'),
    # 货架选择页面
    url(r'^shelfSelect/$', views.shelfSelect, name='shelfSelect'),
    # 钥匙柜选择页面
    url(r'^keyCabinetSelect/$', views.keyCabinetSelect, name='keyCabinetSelect'),
    # 钥匙柜查看页面
    url(r'^keyCabinetView/$', views.keyCabinetView, name='keyCabinetView'),
    # 货架领用页面
    url(r'^shelfUse/$', views.shelfUse, name='shelfUse'),
    # 货架归还页面
    url(r'^shelfReturn/$', views.shelfReturn, name='shelfReturn'),
    # 打印货架二维码页面
    url(r'^printFlowCode/$', views.printFlowCode, name='printFlowCode'),

    # 检材使用页面
    url(r'^materialUse/$', views.materialUse, name='materialUse'),
    # 检材归还页面
    url(r'^materialReturn/$', views.materialReturn, name='materialReturn'),
    # 试剂补货页面
    url(r'^materialSupply/$', views.materialSupply, name='materialSupply'),

    # 检材入库操作
    url(r'^materialStockInDo/$', views.materialStockInDo, name='materialStockInDo'),

    url(r'^getSupplyDrugCategoryListJson/$', views.getSupplyDrugCategoryListJson, name='getSupplyDrugCategoryListJson'),


        # 钥匙柜查看页面
    url(r'^mapFlowView/$', views.mapFlowView, name='mapFlowView'),
]