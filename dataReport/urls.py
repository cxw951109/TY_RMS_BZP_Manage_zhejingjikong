from django.conf.urls import url

from dataReport import views

app_name = 'dataReport'

urlpatterns = [
    # 数据报表首页
    url(r'^index/$', views.index, name='index'),
    # 数据报表（试剂流转记录）
    url(r'^drugRecordList/$', views.drugRecordList, name='drugRecordList'),
    # 数据报表（预警列表）
    url(r'^warningList/$', views.warningList, name='warningList'),
    # 获取预警列表Json数据
    url(r'^getWarningListJson/$', views.getWarningListJson, name='getWarningListJson'),
    # 数据报表（试剂报纸列表）
    url(r'^drugShelfLifeList/$', views.drugShelfLifeList, name='drugShelfLifeList'),
    # 数据报表（用户数据列表）
    url(r'^userList/$', views.userList, name='userList'),
    # 数据报表（用户数据列表）
    url(r'^categoryCountList/$', views.categoryCountList, name='categoryCountList'),
    # 获取客户端信息
    url(r'^getClientListJson/$', views.getClientListJson, name='getClientListJson'),
    #得到操作类型
    url(r'getRecordType/$',views.getRecordType,name='getRecordType'),
    # 数据流转记录数据
    url(r'^getDrugRecordListJson/.*$', views.getDrugRecordListJson, name='getDrugRecordListJson'),
    # 获取流转记录图表
    url(r'^drugRecordChart/$', views.drugRecordChart, name='drugRecordChart'),
    # 获取库存信息概览统计Json数据
    url(r'^getCategoryCountListJson/$', views.getCategoryCountListJson, name='getCategoryCountListJson'),
    # 获取试剂Json数据列表
    url(r'^getDrugListJson/.*$', views.getDrugListJson, name='getDrugListJson'),
    # 试剂保质期统计图
    url(r'^drugShelfLifeChart/$', views.drugShelfLifeChart, name='drugShelfLifeChart'),
    # 获取试剂的Json数据
    url(r'^getDrugShelfLifeChartJson/$', views.getDrugShelfLifeChartJson, name='getDrugShelfLifeChartJson'),
    # 获取试剂资金消耗页面
    url(r'^fundsConsumeChart/$', views.fundsConsumeChart, name='fundsConsumeChart'),
    #  获取试剂资金消耗统计
    url(r'^getFundsConsumeChartJson/$', views.getFundsConsumeChartJson, name='getFundsConsumeChartJson'),
    # 获取试剂库存价值图标
    url(r'^fundsNormalChart/$', views.fundsNormalChart, name='fundsNormalChart'),
    # 获取试剂库存价值Json数据
    url(r'^getFundsNormalChartJson/$', views.getFundsNormalChartJson, name='getFundsNormalChartJson'),
    # 获取试剂流转记录表
    url(r'^getDrugRecordChartJson/$', views.getDrugRecordChartJson, name='getDrugRecordChartJson'),
    # 导出库存试剂信息报表路由
    url(r'^ExportDrugCategoryData/$', views.ExportDrugCategoryData, name='ExportDrugCategoryData'),
    # 导出试剂数据明细报表
    url(r'^exportDrugShelfLifeData/.*?$', views.exportDrugShelfLifeData, name='exportDrugShelfLifeData'),
    # 导出试剂流转记录报表路由
    url(r'^exportDrugRecordData/.*?$', views.exportDrugRecordData, name='exportDrugRecordData'),
    # 导出系统预警数据记录报表
    url(r'^exportWarningData/$', views.exportWarningData, name='exportWarningData'),
    # 导出用户角色统计报表
    url(r'^exportUserData/$', views.exportUserData, name='exportUserData'),
    # 导出报表统计下的所有报表数据 路由
    url(r'^exportAllReportData/$', views.exportAllReportData, name='exportAllReportData'),

    #######################################返回页面#########################
    #库存信息总览
    url(r'^getOverviewInfo/$', views.getOverviewInfo, name='getOverviewInfo'),
    #入库信息查询
    url(r'^getPutInInfo/$', views.getPutInInfo, name='getPutInInfo'),
    #使用频率统计
    url(r'^getUseFrequencyInfo/$', views.getUseFrequencyInfo, name='getUseFrequencyInfo'),
    #消耗统计
    url(r'^getDrugConsumeInfo/$', views.getDrugConsumeInfo, name='getDrugConsumeInfo'),
    #保质期统计
    url(r'^getShelflifeInfo/$', views.getShelflifeInfo, name='getShelflifeInfo'),
    #保质期预警统计
    url(r'^getShelflifeWarning/$', views.getShelflifeWarning, name='getShelflifeWarning'),
    #库存呆滞料统计
    url(r'^getStagnantInfo/$', views.getStagnantInfo, name='getStagnantInfo'),
    #试剂历史使用信息统计
    url(r'^getDrugUseRecordInfo/$', views.getDrugUseRecordInfo, name='getDrugUseRecordInfo'),


    #人员用量统计
    url(r'^getUserConsumeInfo/$', views.getUserConsumeInfo, name='getUserConsumeInfo'),
    #试剂种类消耗统计
    url(r'^getDrugUseCategotyConsumeInfo/$', views.getDrugUseCategotyConsumeInfo, name='getDrugUseCategotyConsumeInfo'),
    #试剂明细信息统计
    url(r'^getDrugDetailInfo/$', views.getDrugDetailInfo, name='getDrugDetailInfo'),

    ##################################返回数据##############################
    #返回库存总览json数据
    url(r'^getOverviewInfoJson/$', views.getOverviewInfoJson, name='getOverviewInfoJson'),
    #返回入库信息json数据
    url(r'^getPutInInfoJson/$', views.getPutInInfoJson, name='getPutInInfoJson'),
    #返回使用频率json数据
    url(r'^getUseFrequencyInfoJson/$', views.getUseFrequencyInfoJson, name='getUseFrequencyInfoJson'),
    #返回消耗统计json数据
    url(r'^getDrugConsumeInfoJson/$', views.getDrugConsumeInfoJson, name='getDrugConsumeInfoJson'),
    #返回保质期统计json数据
    url(r'^getShelflifeInfoJson/$', views.getShelflifeInfoJson, name='getShelflifeInfoJson'),
    #返回保质期预警统计json数据
    url(r'^getShelflifeWarningJson/$', views.getShelflifeWarningJson, name='getShelflifeWarningJson'),
    #返回库存呆滞json数据
    url(r'^getStagnantInfoJson/$', views.getStagnantInfoJson, name='getStagnantInfoJson'),
    #返回试剂历史使用json数据
    url(r'^getDrugUseRecordInfoJson/$', views.getDrugUseRecordInfoJson, name='getDrugUseRecordInfoJson'),

    #返回人员用量统计json数据
    url(r'^getUserConsumeInfoJson/$', views.getUserConsumeInfoJson, name='getUserConsumeInfoJson'),
    #返回试剂种类消耗统计json数据
    url(r'^getDrugUseCategotyConsumeInfoJson/$', views.getDrugUseCategotyConsumeInfoJson, name='getDrugUseCategotyConsumeInfoJson'),
    #返回试剂明细信息统计json数据
    url(r'^getDrugDetailInfoJson/$', views.getDrugDetailInfoJson, name='getDrugDetailInfoJson'),

    #####################################下载报表#################################
    #下载库存总览表
    url(r'^downOverviewInfo/$', views.downOverviewInfo, name='downOverviewInfo'),
    #下载入库信息表
    url(r'^downPutInInfo/$', views.downPutInInfo, name='downPutInInfo'),
    #下载使用频率报表
    url(r'^downUseFrequencyInfo/$', views.downUseFrequencyInfo, name='downUseFrequencyInfo'),
    #下载消耗统计报表
    url(r'^downDrugConsumeInfo/$', views.downDrugConsumeInfo, name='downDrugConsumeInfo'),
    #下载保质期统计报表
    url(r'^downShelflifeInfo/$', views.downShelflifeInfo, name='downShelflifeInfo'),
    #下载保质期预警统计报表
    url(r'^downShelflifeWarning/$', views.downShelflifeWarning, name='downShelflifeWarning'),
    #下载库存呆滞表
    url(r'^downStagnantInfo/$', views.downStagnantInfo, name='downStagnantInfo'),
    #下载试剂历史使用表
    url(r'^downDrugUseRecordInfo/$', views.downDrugUseRecordInfo, name='downDrugUseRecordInfo'),
    #下载人员用量统计报表
    url(r'^downUserConsumeInfo/$', views.downUserConsumeInfo, name='downUserConsumeInfo'),
    #下载试剂种类消耗统计报表
    url(r'^downDrugUseCategotyConsumeInfo/$', views.downDrugUseCategotyConsumeInfo, name='downDrugUseCategotyConsumeInfo'),
    #下载人员消耗试剂信息统计报表
    url(r'^downUserConsumeInfoJson/$', views.downUserConsumeInfoJson,name='downUserConsumeInfoJson'),
    #下载试剂种类消耗信息统计报表
    url(r'^downDrugUseCategotyConsumeInfoJson/$', views.downDrugUseCategotyConsumeInfoJson,name='downDrugUseCategotyConsumeInfoJson'),



]
