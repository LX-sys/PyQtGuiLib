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

        self.rect_ = QRect(50,50,200,100)

        # 将动画框架的作用对象设置在 绘图上
        self.ani = Animation(self,ani_obj_mode=Animation.Draw)
        self.ani.setDuration(5000)

        # 左测图
        self.poly = QPolygon([QPoint(50+300,50+10),
                   QPoint(200+300,50),
                   QPoint(200+300,150+10),
                   QPoint(50+300,150)])
        # 中间图
        self.mid_ply = QPolygon([QPoint(50+200,50),
                   QPoint(200+200,50),
                   QPoint(200+200,150),
                   QPoint(50+200,150)])

        self.image = QPixmap(r'D:\code\PyQtGuiLib\tests\temp_image\python1.png')
        self.mid_image = QPixmap(r'D:\code\PyQtGuiLib\tests\temp_image\python1.png')

        self.ani.addAni({
            "propertyName": b"point",
            "duration": 3000,
            "sv": self.poly[0],
            "ev": QPoint(50+300,50),
        })
        self.ani.addAni({
            "propertyName": b"point",
            "duration": 3000,
            "sv": self.poly[2],
            "ev": QPoint(200+300,150),
        })

        self.ani.start()

    def test_call(self,obj,a,b):
        print("===============")
        print(self.rect_)
        print("绘图动画完成",obj,a,b)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        scaled_image = self.image.scaled(QSize(150, 150))
        scaled_image_mid = self.mid_image.scaled(QSize(150, 150))

        # 绘制中间图
        # painter.setBrush(QColor(255, 0, 0))
        painter.drawPolygon(self.mid_ply)
        painter.drawPixmap(self.mid_ply.boundingRect(), scaled_image_mid)

        # 绘制左侧图
        # painter.setBrush(QColor(0, 255, 0))
        painter.drawPolygon(self.poly)
        painter.drawPixmap(self.poly.boundingRect(), scaled_image)


        # 绘制
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())