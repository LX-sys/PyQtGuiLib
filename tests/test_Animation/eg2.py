# -*- coding:utf-8 -*-
# @time:2023/3/817:11
# @author:LX
# @file:eg2.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPoint,
    qt,
    QPushButton,
    Qt,
    QPalette,
    QColor,
    QPaintEvent,
    QPainter,
    QBrush,
    QSize,
    QMainWindow,
    QLineEdit,
    desktopCenter,
    QPixmap,
    QLinearGradient,
    QLabel,
    QFont,
    textSize,
    QFontMetricsF,
    Qt,
    QMouseEvent,
    QVBoxLayout,
    QPropertyAnimation,
    QRect,
    QObject,
    QPoint,
    QPolygon,
)

import time
from PyQt5.QtWidgets import QSplashScreen,QDialog,QProxyStyle,QButtonGroup
from PyQt5.QtCore import QThread,QRunnable,QThreadPool
from PyQt5.QtGui import QFontMetrics,QFocusEvent


'''
    动画框架测试
'''
from PyQtGuiLib.core.resolver import dumpStructure
from functools import partial

from PyQtGuiLib.animation import Animation


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)
        self.r = 0

        self.rect_ = QRect(200,250,200,100)


        # 将动画框架的作用对象设置在 绘图上
        self.ani = Animation(self,ani_obj_mode=Animation.Draw)
        self.ani.setDuration(5000)
        # self.ani.setAniMode(Animation.Sequential)

        # self.ani.addAni({
        #     # "targetObj": QObject(),
        #     "propertyName": b"geometry",
        #     "duration":3000,
        #     "sv": self.rect_,
        #     "ev": QRect(300,200,100,100),
        #     # "call":self.test_call,
        #     # "argc":(1,2)
        # })
        # self.ani.addAni({
        #     # "targetObj": QObject(),
        #     "propertyName": b"size",
        #     "duration":3000,
        #     "sv": self.rect_,
        #     "ev": QRect(0,0,300,300),
        #     "call":self.test_call,
        #     "argc":(1,2)
        # })
        # self.ani.addAni({
        #     # "targetObj": QObject(),
        #     "propertyName": b"pos",
        #     "duration":3000,
        #     "sv": self.rect_,
        #     "ev": QRect(300,300,0,0),
        #     "call":self.test_call,
        #     "argc":(1,2)
        # })
        self.rotate_a = self.ani.objPack(0)
        self.ani.addAni({
            # "targetObj": QObject(),
            "propertyName": b"rotate",
            "duration": 3000,
            "sv": self.rotate_a,
            "ev": self.ani.objPack(360),
            "call": self.test_call,
            "argc": (1, 2)
        })
        # self.ani.addSeriesAni(
        #     {
        #         # "targetObj": QObject(),
        #         "propertyName": b"geometry",
        #         "duration": 3000,
        #         "sv": self.rect_,
        #         "ev": QRect(300, 200, 50, 200),
        #         # "call": self.test_call,
        #         # "argc": (1, 2)
        #     },
        #     # []
        #     [QRect(50, 200, 100, 100),
        #      # QRect(150, 50, 100, 100)
        #      ]
        # )

        self.ani.start()

    def test_call(self,obj,a,b):
        print("===============")
        print(self.rect_)
        print("绘图动画完成",obj,a,b)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setBrush(QColor(0,255,0))
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        painter.rotate(self.rotate_a.valve())
        painter.drawRoundedRect(self.rect_,self.r,self.r)
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())