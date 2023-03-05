# -*- coding:utf-8 -*-
# @time:2023/1/819:02
# @author:LX
# @file:1.py
# @software:PyCharm

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQtGuiLib.abandonCase.widgets import BorderlessWidget

class RoundShadow(BorderlessWidget):
    """圆角边框类"""


    def __init__(self, parent=None):
        super(RoundShadow, self).__init__(parent)
        self.border_width = 5
        # 设置 窗口无边框和背景透明 *必须
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)


    def paintEvent(self, event):
        # 阴影
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        pat.fillPath(path, QBrush(Qt.white))

        
        color = QColor(192, 192, 192, 50)
        # color = QColor(255, 0, 0, 255)
        for i in range(10):
            i_path = QPainterPath()
            i_path.setFillRule(Qt.WindingFill)
            ref = QRectF(10 - i, 10 - i, self.width() - (10 - i) * 2, self.height() - (10 - i) * 2)
            i_path.addRect(ref)
            i_path.addRoundedRect(ref, self.border_width, self.border_width)
            # print(150 - i ** 0.5 * 50)
            color.setAlpha(150 - i ** 0.5 * 50)
            pat.setPen(color)
            pat.drawPath(i_path)

        # 圆角
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
        pat2.setBrush(Qt.white)
        pat2.setPen(Qt.transparent)

        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width() - 9)
        rect.setHeight(rect.height() - 9)
        pat2.drawRoundedRect(rect, 8, 8)


class TestWindow(RoundShadow):
    """测试窗口"""


    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)

        self.resize(300, 300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = RoundShadow()
    t.show()
    app.exec_()
