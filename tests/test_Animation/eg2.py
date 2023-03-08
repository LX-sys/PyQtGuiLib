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
    QObject
)

import time
from PyQt5.QtWidgets import QSplashScreen,QDialog,QProxyStyle,QButtonGroup
from PyQt5.QtCore import QThread,QRunnable,QThreadPool
from PyQt5.QtGui import QFontMetrics,QFocusEvent

# QSplashScreen
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

        self.rect_ = QRect(50,50,100,100)
        self.rect_.height()
        self.rect_.width()

        # 将动画框架的作用对象设置在 绘图上
        self.ani = Animation(self,ani_obj_mode=Animation.Draw)
        self.ani.setDuration(5000)

        self.ani.addAni({
            # "targetObj": QObject(),
            "propertyName": b"size",
            "duration":3000,
            "sv": self.rect_,
            "ev": QRect(50,50,300,300),
        })
        self.ani.start()

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setBrush(QColor(0,255,0))
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