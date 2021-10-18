
// 验收单打印配置模型
var acceptanceOrderPrintJson = {
    "panels": [{
        "index": 0,
        "paperType": "A3",
        "height": 297,
        "width": 420,
        "paperHeader": 109.5,
        "paperFooter": 736.5,
        "printElements": [{
            "options": {
                "left": 523.5,
                "top": 54,
                "height": 9.75,
                "width": 211.5,
                "title": "标准品验收单",
                "fontSize": 21.75,
                "fontWeight": "bold"
            },
            "printElementType": {
                "type": "text"
            }
        },
        {
            "options": {
                "left": 40.5,
                "top": 85.5,
                "height": 9,
                "width": 1107,
                "borderColor": "#cc3d80"
            },
            "printElementType": {
                "type": "hline"
            }
        },
        {
            "options": {
                "left": 736.5,
                "top": 94.5,
                "height": 9.75,
                "width": 196.5,
                "title": "创建人",
                "field": "CreateUserName",
                "fontWeight": "bold",
                "color": "#cc3d80",
                "fontSize": 13.5
            },
            "printElementType": {
                "type": "text"
            }
        },
        {
            "options": {
                "left": 43.5,
                "top": 94.5,
                "height": 9.75,
                "width": 213,
                "title": "验收单号",
                "field": "AcceptanceOrderCode",
                "fontWeight": "bold",
                "color": "#cc3d80",
                "fontSize": 13.5
            },
            "printElementType": {
                "type": "text"
            }
        },
        {
            "options": {
                "left": 937.5,
                "top": 94.5,
                "height": 9.75,
                "width": 210,
                "title": "创建时间",
                "field": "CreateDate",
                "fontWeight": "bold",
                "color": "#cc3d80",
                "fontSize": 13.5
            },
            "printElementType": {
                "type": "text"
            }
        },
        {
            "options": {
                "left": 42,
                "top": 117,
                "height": 124.5,
                "width": 1105.5,
                "textAlign": "center",
                "tableHeaderFontWeight": "bold",
                "field": "table",
                "tableHeaderRowHeight": 36,
                "tableHeaderFontSize": 12,
                "tableBodyRowHeight": 36,
                "columns": [[{
                    "title": "序号",
                    "field": "SortIndex",
                    "width": 23.17281609166604,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true
                },
                {
                    "title": "标准品名称",
                    "field": "DrugName",
                    "width": 55.00582260479753,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "DrugName"
                },
                {
                    "title": "批次号",
                    "field": "DrugCode",
                    "width": 55.33839606568104,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "DrugCode"
                },
                {
                    "title": "规格",
                    "field": "Speci",
                    "width": 55.62098785339474,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "Speci"
                },
                {
                    "title": "包装完好",
                    "field": "PackageStatus",
                    "width": 54.44849708549196,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "PackageStatus"
                },
                {
                    "title": "标识完好",
                    "field": "MarkStatus",
                    "width": 55.338882114455025,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "MarkStatus"
                },
                {
                    "title": "证书对应性",
                    "field": "CertificateStatus",
                    "width": 61.11262833743357,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "CertificateStatus"
                },
                {
                    "title": "证书信息",
                    "width": 100,
                    "colspan": 2,
                    "rowspan": 1,
                    "checked": true
                },
                {
                    "title": "检测方法",
                    "field": "DetectionMethod",
                    "width": 53.634246783698245,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "DetectionMethod"
                },
                {
                    "title": "检测信息",
                    "width": 60,
                    "colspan": 2,
                    "rowspan": 1,
                    "checked": true
                },
                {
                    "title": "基本组成",
                    "field": "BasicComponent",
                    "width": 54.68037325794143,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "BasicComponent"
                },
                {
                    "title": "购入日期",
                    "field": "BuyDate",
                    "width": 53.45663888187448,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "BuyDate"
                },
                {
                    "title": "购入数量",
                    "field": "Count",
                    "width": 41.335131309624586,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "Count"
                },
                {
                    "title": "生产商",
                    "field": "Manufacturer",
                    "width": 54.59754375504451,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "Manufacturer"
                },
                {
                    "title": "保存条件",
                    "field": "StorageConditions",
                    "width": 47.01587775803667,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "StorageConditions"
                },
                {
                    "title": "安全防护",
                    "field": "Security",
                    "width": 54.75531390012025,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "Security"
                },
                {
                    "title": "特殊运输要求",
                    "field": "SpecialRequirements",
                    "width": 45.31526036411275,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "SpecialRequirements"
                },
                {
                    "title": "验收人",
                    "field": "AcceptanceUserName",
                    "width": 46.78070346223948,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "AcceptanceUserName"
                },
                {
                    "title": "验收结论",
                    "field": "AcceptanceComment",
                    "width": 43.172340687779815,
                    "colspan": 1,
                    "rowspan": 2,
                    "checked": true,
                    "columnId": "AcceptanceComment"
                }], [{
                    "title": "特性量值",
                    "field": "CertCharaValue",
                    "width": 63.00685764270999,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true,
                    "columnId": "CertCharaValue"
                },
                {
                    "title": "不确定度",
                    "field": "CertUncertainty",
                    "width": 62.19986531364934,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true,
                    "columnId": "CertUncertainty"
                },
                {
                    "title": "特性量值",
                    "field": "DetectionCharaValue",
                    "width": 63.08877330266447,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true,
                    "columnId": "DetectionCharaValue"
                },
                {
                    "title": "不确定度",
                    "field": "DetectionUncertainty",
                    "width": 62.42304342758412,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true,
                    "columnId": "DetectionUncertainty"
                }]]
            },
            "printElementType": {
                "title": "表格",
                "type": "tableCustom"
            }
        },
        {
            "options": {
                "left": 757.5,
                "top": 759,
                "height": 36,
                "width": 106.5,
                "src": "/Content/assets/hi.png",
                "field": "SignUrl"
            },
            "printElementType": {
                "type": "image"
            }
        },
        {
            "options": {
                "left": 666,
                "top": 772.5,
                "height": 9.75,
                "width": 210,
                "title": "验收人签字",
                "fontSize": 12,
                "fontWeight": "bold",
                "field": "666"
            },
            "printElementType": {
                "type": "text"
            }
        },
        {
            "options": {
                "left": 912,
                "top": 774,
                "height": 9.75,
                "width": 232.5,
                "title": "签字日期",
                "fontSize": 12,
                "fontWeight": "bold",
                "field": "AcceptanceDate"
            },
            "printElementType": {
                "type": "text"
            }
        }],
        "paperNumberLeft": 1160,
        "paperNumberTop": 819
    }]
}

// 采购单打印配置模型
var purchaseOrderPrintJson={
    "panels": [{
        "index": 0,
        "paperType": "A3",
        "height": 420,
        "width": 297,
        "paperHeader": 121.5,
        "paperFooter": 1036.5,
        "printElements": [{
            "options": {
                "left": 361.5,
                "top": 63,
                "height": 9.75,
                "width": 145.5,
                "title": "标准品采购单",
                "fontSize": 21.75,
                "fontWeight": "bolder"
            },
            "printElementType": {
                "type": "text"
            }
        },
        {
            "options": {
                "left": 34.5,
                "top": 94.5,
                "height": 9,
                "width": 771,
                "borderStyle": "dotted"
            },
            "printElementType": {
                "type": "hline"
            }
        },
        {
            "options": {
                "left": 39,
                "top": 105,
                "height": 9.75,
                "width": 261,
                "title": "采购单号",
                "field": "PurchaseOrderCode",
                "testData": "1020200229185924552",
                "fontWeight": "bold",
                "fontSize": 13.5,
                "color": "#cc3d80"
            },
            "printElementType": {
                "type": "text"
            }
        },
        {
            "options": {
                "left": 397.5,
                "top": 105,
                "height": 9.75,
                "width": 184.5,
                "title": "创建人",
                "field": "CreateUserName",
                "testData": "管理员",
                "fontWeight": "bold",
                "fontSize": 13.5,
                "color": "#cc3d80"
            },
            "printElementType": {
                "type": "text"
            }
        },
        {
            "options": {
                "left": 594,
                "top": 105,
                "height": 9.75,
                "width": 219,
                "title": "创建时间",
                "field": "CreateDate",
                "testData": "2020-3-1 15:26:55",
                "fontWeight": "bold",
                "fontSize": 13.5,
                "color": "#cc3d80"
            },
            "printElementType": {
                "type": "text"
            }
        },
        {
            "options": {
                "left": 33,
                "top": 129,
                "height": 81,
                "width": 772.5,
                "textAlign": "center",
                "tableHeaderFontWeight": "bold",
                "field": "table",
                "tableHeaderRowHeight": 36,
                "tableHeaderFontSize": 12,
                "tableBodyRowHeight": 36,
                "columns": [[{
                    "title": "序号",
                    "field": "SortIndex",
                    "width": 62.223962649550806,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true
                },
                {
                    "title": "标准品名称",
                    "field": "DrugName",
                    "width": 211.511023804147,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true
                },
                {
                    "title": "CAS码",
                    "field": "CASNumber",
                    "width": 132.40268465302807,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true
                },
                {
                    "title": "规格",
                    "field": "Speci",
                    "width": 93.76217335433806,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true
                },
                {
                    "title": "单位",
                    "field": "SpeciUnit",
                    "width": 93.3975223500384,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true
                },
                {
                    "title": "纯度",
                    "field": "Purity",
                    "width": 101.05816267905118,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true
                },
                {
                    "title": "采购数量",
                    "field": "Count",
                    "width": 78.14447050984646,
                    "colspan": 1,
                    "rowspan": 1,
                    "checked": true
                }]]
            },
            "printElementType": {
                "title": "表格",
                "type": "tableCustom"
            }
        },
        {
            "options": {
                "left": 124.5,
                "top": 757.5,
                "height": 69,
                "width": 121.5
            },
            "printElementType": {
                "title": "html",
                "type": "html"
            }
        },
        {
            "options": {
                "left": 37.5,
                "top": 1047,
                "height": 9,
                "width": 771
            },
            "printElementType": {
                "type": "hline"
            }
        },
        {
            "options": {
                "left": 130.5,
                "top": 1053,
                "height": 40.5,
                "width": 108,
                "src": "/Content/assets/hi.png",
                "field": "SignUrl1"
            },
            "printElementType": {
                "type": "image"
            }
        },
        {
            "options": {
                "left": 43.5,
                "top": 1072.5,
                "height": 9.75,
                "width": 90,
                "title": "审批人1签字",
                "field": "ApproveUserName1",
                "fontSize": 12,
                "fontWeight": "bold"
            },
            "printElementType": {
                "type": "text"
            }
        },
        {
            "options": {
                "left": 45,
                "top": 1114.5,
                "height": 9.75,
                "width": 204,
                "title": "签字日期",
                "field": "ApproveDate1",
                "fontSize": 12,
                "fontWeight": "bold"
            },
            "printElementType": {
                "type": "text"
            }
        }],
        "paperNumberLeft": 811,
        "paperNumberTop": 1168,
        "rotate": true
    }]
}