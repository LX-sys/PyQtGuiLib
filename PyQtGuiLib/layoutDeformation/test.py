# -*- coding:utf-8 -*-
# @time:2023/3/411:37
# @author:LX
# @file:test.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
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
    QPropertyAnimation,
    QRect,
    QParallelAnimationGroup,
    QResizeEvent
)
from PyQtGuiLib.core.flowLayout import FlowLayout
import time
from PyQt5.QtWidgets import QSplashScreen,QDialog,QProxyStyle,QButtonGroup
from PyQt5.QtCore import QThread,QRunnable,QThreadPool
from PyQt5.QtGui import QFontMetrics,QFocusEvent

# QSplashScreen
'''
    测试用例的标准模板,该代码用于复制
'''
from PyQtGuiLib.core.resolver import dumpStructure
from PyQtGuiLib.styles import ButtonStyle


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.a = QWidget(self)
        self.b = QWidget(self)
        self.a.setObjectName("a")
        self.b.setObjectName("b")

        self.a.resize(self.width(),150)
        self.b.resize(self.width(),self.height()-150)
        self.b.move(0,150)

        self.setStyleSheet('''
#a{
border:1px solid red;
}
#b{
border:1px solid blue;
}
        ''')

        # ---
        self.af = FlowLayout(self.a)
        self.bf = FlowLayout(self.b)

        for ai in range(8):
            btn = QPushButton("test_{}".format(ai))
            btn.setFixedSize(100,50)
            btn.setStyleSheet(ButtonStyle.randomStyle())  # 使用 皮肤包
            self.af.addWidget(btn)

        for bi in range(10):
            btn = QPushButton("test_{}".format(bi))
            btn.setFixedSize(130, 60)
            btn.setStyleSheet(ButtonStyle.randomStyle())  # 使用 皮肤包
            self.bf.addWidget(btn)


        self.isf = False
        self.btn = QPushButton("开始 影像形变-布局",self)
        self.btn.resize(150,60)
        self.btn.move(300,300)
        self.btn.clicked.connect(self.test_start)
        # self.anim()

    def test_start(self):
        if self.isf is False:
            self.anim()
            self.btn.setText("恢复 影像形变-布局")
            self.isf = True
        else:
            self.anim_re()
            self.btn.setText("开始 影像形变-布局")
            self.isf = False


    def anim(self):
        pain = QParallelAnimationGroup(self)
        # pain.setDirection(3000)

        ani = QPropertyAnimation(self.a,b"geometry",self)
        ani.setDuration(1000)
        ani.setStartValue(self.a.rect())
        ani.setEndValue(QRect(self.a.x(),self.a.y(),
                              self.a.height(),self.a.width()))


        anib = QPropertyAnimation(self.b,b"geometry",self)
        anib.setDuration(1000)
        anib.setStartValue(self.b.rect())
        anib.setEndValue(QRect(150,0,
                              self.b.width()-150,self.height()))

        pain.addAnimation(ani)
        pain.addAnimation(anib)
        pain.start()


    def anim_re(self):
        pain = QParallelAnimationGroup(self)
        # pain.setDirection(3000)

        ani = QPropertyAnimation(self.a, b"geometry", self)
        ani.setDuration(1000)
        ani.setStartValue(self.a.rect())
        ani.setEndValue(QRect(self.a.x(), self.a.y(),
                              self.a.height(), self.a.width()))

        anib = QPropertyAnimation(self.b, b"geometry", self)
        anib.setDuration(1000)
        anib.setStartValue(self.b.rect())
        anib.setEndValue(QRect(0, 150,
                               self.width(), self.height()- 150))

        pain.addAnimation(ani)
        pain.addAnimation(anib)
        pain.start()


    def resizeEvent(self, e: QResizeEvent) -> None:
        self.a.resize(self.width(), 150)
        self.b.resize(self.width(), self.height() - 150)
        super().resizeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())