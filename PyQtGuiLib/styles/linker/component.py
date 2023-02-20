# -*- coding:utf-8 -*-
# @time:2023/2/209:09
# @author:LX
# @file:component.py
# @software:PyCharm
'''
    小组件
'''
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QGroupBox,
    QFormLayout,
    QPushButton,
    QSize,
    QLabel
)
from PyQtGuiLib.core import PaletteFrame
from PyQtGuiLib.styles import QssStyleAnalysis

# 通用 QGroupBox 大小
PUBLIC_GROUPBOX_SIZE = QSize(150,100)


# 颜色组件
# class GroupBox(QGroupBox):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)



# 通用的颜色组件
def colorComponent(self,parent):
    '''

    :param self: StyleLinker 对象
    :param parent: parent 窗口对象
    :param browser:  QTextBrowser 对象
    :return:
    '''

    def open_PaletteFrame(case:str):
        p = PaletteFrame()  # 创建颜色版
        p.show()

        def updateBG(rgba,key):
            if self.global_select is None:
                head = self.global_var.header()[0]
            else:
                head = self.global_select
            self.global_var.selector(head).updateAttr(key,
                                                      "rgba(%s, %s, %s,%s)" % rgba)
            self.browser().clear()
            self.browser().append(self.global_var.toStr())

        if case == "bg":
            p.setWindowTitle("背景色")
            p.rgbaChange.connect(lambda rgba:updateBG(rgba,"background-color"))
        if case == "c":
            p.setWindowTitle("前景色")
            p.rgbaChange.connect(lambda rgba: updateBG(rgba, "color"))


    groupBox = QGroupBox(parent)
    groupBox.setTitle("调色区")
    groupBox.resize(PUBLIC_GROUPBOX_SIZE)
    fboy = QFormLayout(groupBox)

    bgc = QLabel("背景颜色")
    bgc_btn = QPushButton()
    color = QLabel("前景色")
    color_btn = QPushButton()
    fboy.addRow(bgc,bgc_btn)
    fboy.addRow(color,color_btn)

    # event
    bgc_btn.clicked.connect(lambda: open_PaletteFrame("bg"))
    color_btn.clicked.connect(lambda: open_PaletteFrame("c"))