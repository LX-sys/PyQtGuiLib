# -*- coding:utf-8 -*-
# @time:2023/3/711:45
# @author:LX
# @file:eg1.py
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
    QRect
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

        self.btn = QPushButton("测试",self)
        self.btn.setStyleSheet('''
QPushButton{
background-color: red;
font-size:18px;
}
        ''')
        self.btn.move(50,50)
        self.btn.resize(130,60)

        # 标记
        self.p = True
        self.btn_pause = QPushButton("暂停动画",self)
        self.btn_pause.move(150,50)
        self.btn_pause.resize(130,30)

        self.ani = Animation(self)
        self.ani.setDuration(5000)

        self.ani.addAni({
            "targetObj":self.btn,
            "propertyName":b"geometry",
            "sv":self.btn.rect(),
            "special":Animation.InCurve,
            "ev":QRect(150,150,300,300),
            "call":self.test,
            "argc":(234,"hello")
        })
        self.ani.addAni({
            "targetObj":self.btn,
            "propertyName":b"backgroundColor",
            "sv":QColor(255, 0, 0),
            "ev":QColor(0, 255, 0),
            "selector":"QPushButton"
        })
        self.ani.addAni({
            "targetObj":self.btn,
            "propertyName":b"fontSize",
            "sv":18,
            "ev":50,
            "selector":"QPushButton"
        })
        self.ani.start()

        self.btn_pause.clicked.connect(lambda :self.ani.aniSwitch(self.btn_pause))

    def test(self,obj:QPushButton,a,b):
        print(obj)
        obj.setText("执行完成")
        print("Ddas",a,b)

    def test_pause(self):
        if self.p:
            self.ani.pause()
            self.p = False
            self.btn_pause.setText("恢复动画")
        else:
            self.ani.resume()
            self.p = True
            self.btn_pause.setText("暂停动画")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())