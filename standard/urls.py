from django.conf.urls import url

from . import views

app_name = 'standard'

urlpatterns = [
    # 采购列表页面
    url(r'^purchaseIndex/$', views.purchaseIndex, name='purchaseIndex'),
    # 等待采购列表页面
    url(r'^purchaseWaitingIndex/$', views.purchaseWaitingIndex, name='purchaseWaitingIndex'),
    # 采购完成列表页面
    url(r'^purchaseCompleteIndex/$', views.purchaseCompleteIndex, name='purchaseCompleteIndex'),
    # 验收列表页面
    url(r'^acceptanceIndex/$', views.acceptanceIndex, name='acceptanceIndex'),
    # 期间核查列表页面
    url(r'^periodCheckIndex/$', views.periodCheckIndex, name='periodCheckIndex'),
    # 期间核查试剂列表页面
    url(r'^periodCheckDrugIndex/$', views.periodCheckDrugIndex, name='periodCheckDrugIndex'),
    # 即时期间核查页面
    url(r'^periodCheckDrugAnonIndex/$', views.periodCheckDrugAnonIndex, name='periodCheckDrugAnonIndex'),

    # 采购表单页面
    url(r'^purchaseForm/$', views.purchaseForm, name='purchaseForm'),
    # 采购试剂表单页面
    url(r'^purchaseDrugForm/$', views.purchaseDrugForm, name='purchaseDrugForm'),
    # 验收表单页面
    url(r'^acceptanceForm/$', views.acceptanceForm, name='acceptanceForm'),
    # 验收试剂表单页面
    url(r'^acceptanceDrugForm/$', views.acceptanceDrugForm, name='acceptanceDrugForm'),
    # 期间核查表单页面
    url(r'^periodCheckForm/$', views.periodCheckForm, name='periodCheckForm'),
    # 期间核查试剂表单页面
    url(r'^periodCheckDrugForm/$', views.periodCheckDrugForm, name='periodCheckDrugForm'),
    # 拍照上传表单页面
    url(r'^photographForm/$', views.photographForm, name='photographForm'),
    # 裁剪图片表单
    url(r'^cropperImgForm/$', views.cropperImgForm, name='cropperImgForm'),
    # 期间核查查看页面
    url(r'^periodCheckView/$', views.periodCheckView, name='periodCheckView'),
    # 试剂期间核查查看页面
    url(r'^periodCheckDrugDetailedInfo/$', views.periodCheckDrugDetailedInfo, name='periodCheckDrugDetailedInfo'),
    # 试剂期间核查不合适页面
    url(r'^periodCheckDrugFailureIndex/$', views.periodCheckDrugFailureIndex, name='periodCheckDrugFailureIndex'),

    
    # 采购查看页面
    url(r'^purchaseView/$', views.purchaseView, name='purchaseView'),
    # 验收查看页面
    url(r'^acceptanceView/$', views.acceptanceView, name='acceptanceView'),
    # 验收单PDF文件导出预览
    url(r'^acceptancePDFView/$', views.acceptancePDFView, name='acceptancePDFView'),
    # 采购单PDF文件导出预览
    url(r'^purchasePDFView/$', views.purchasePDFView, name='purchasePDFView'),


    # 联想搜索试剂
    url(r'^autoSearchDrugList/$', views.autoSearchDrugList, name='autoSearchDrugList'),
    # 获取采购单数据列表
    url(r'^getPurchaseOrderListJson/$', views.getPurchaseOrderListJson, name='getPurchaseOrderListJson'),
    # 获取验收单数据列表
    url(r'^getAcceptanceOrderListJson/$', views.getAcceptanceOrderListJson, name='getAcceptanceOrderListJson'),
    # 获取等待采购数据列表
    url(r'^getWaitingPurchaseListJson/$', views.getWaitingPurchaseListJson, name='getWaitingPurchaseListJson'),
    # 获取完成数据列表
    url(r'^getCompletePurchaseListJson/$', views.getCompletePurchaseListJson, name='getCompletePurchaseListJson'),
    # 获取期间核查数据列表
    url(r'^getPeriodCheckListJson/$', views.getPeriodCheckListJson, name='getPeriodCheckListJson'),
    # 获取期间核查详细数据列表
    url(r'^getPeriodCheckDetailedListJson/$', views.getPeriodCheckDetailedListJson, name='getPeriodCheckDetailedListJson'),
    # 获取期间核查不合格数据列表
    url(r'^getPeriodCheckFailureListJson/$', views.getPeriodCheckFailureListJson, name='getPeriodCheckFailureListJson'),

    # 保存采购数据
    url(r'^savePurchaseOrderData/$', views.savePurchaseOrderData, name='savePurchaseOrderData'),
    # 删除采购单
    url(r'^deletePurchaseOrder/$', views.deletePurchaseOrder, name='deletePurchaseOrder'),
    # 设置完成采购
    url(r'^setCompletePurchase/$', views.setCompletePurchase, name='setCompletePurchase'),
    # 保存拍照信息
    url(r'^savePhotographData/$', views.savePhotographData, name='savePhotographData'),
    # 保存验收单数据
    url(r'^saveAcceptanceOrderData/$', views.saveAcceptanceOrderData, name='saveAcceptanceOrderData'),
    # 保存期间核查数据
    url(r'^savePeriodCheckData/$', views.savePeriodCheckData, name='savePeriodCheckData'),
    # 保存期间核查详细数据
    url(r'^savePeriodCheckDetailedData/$', views.savePeriodCheckDetailedData, name='savePeriodCheckDetailedData'),
    # 导出PDF
    url(r'^exportPDF/$', views.exportPDF, name='exportPDF'),
]