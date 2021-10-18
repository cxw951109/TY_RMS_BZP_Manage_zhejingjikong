"""
此文件是用来生成Code128条形码 并实现打印功能
"""
import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtPrintSupport import QPrinter
from pystrich.code128 import Code128Encoder

import uuid


class CreateBarcode:

    """
            Code128Encoder(options={}) options参数
        * ttf_font：用于呈现标签的truetype字体文件的绝对路径
        * ttf_fontsize：绘制标签的字体大小
        * label_border：条形码和标签之间的像素空间数
        * bottom_border：标签和底部边框之间的像素空间数
        * height：图像的高度（以像素为单位）
        * show_label：是否在条形码下面显示标签（默认为True）“”
    """
    def __init__(self):
        pass

    def create_Code128_img(self, barcode):
        a = Code128Encoder(barcode, options={
            'ttf_font': r'E:\web\TY_RMS_Multiple_Manage\static\fonts\arial.ttf',
            'label_border': 0, 'height': 92,  'bottom_border': 0,
        })
        # bar_width 条码宽度尺寸
        file_name = str(uuid.uuid4()) + '.png'
        a.save(file_name, bar_width=2)
        self.printer_code(file_name)

    def printer_code(self, file_name):
        print(file_name, 55555555)
        a = QApplication([])
        document = QTextDocument()
        html = """
        <head>
        <title>Report</title>
        <style>
        </style>
        </head>
        <body>
        <img src="{}">
        </body>
        """.format(file_name)

        document.setHtml(html)
        printer = QPrinter()
        # 设置纸张到条码的边距  左上下右
        printer.setPageMargins(8, 6, 5, 5, QPrinter.Millimeter)

        document.setPageSize(QSizeF(printer.pageRect().size()))

        print(document.pageSize(), printer.resolution(), printer.pageRect())
        print('正在打印中。。。。')
        document.print_(printer)
        print('打印完成。。')
        os.remove(file_name)


if __name__ == '__main__':
    CreateBarcode().create_Code128_img('100080')
