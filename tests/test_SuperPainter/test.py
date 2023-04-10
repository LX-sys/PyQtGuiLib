# -*- coding:utf-8 -*-
# @time:2023/4/1010:09
# @author:LX
# @file:test.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    PYQT_VERSIONS,
    sys,
    QWidget,
    QPainter,
    QPen,
    QBrush,
    QFont,
    qt,
    Qt,
    QColor,
    QPaintEvent,
    QPushButton,
    QRect
)

from PyQtGuiLib.animation import Animation
from PyQtGuiLib.styles import SuperPainter

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)
        self.painter = SuperPainter()
        self.btn = QPushButton("变大",self)
        self.btn2 = QPushButton("变小",self)
        self.btn.move(300,50)
        self.btn2.move(380,50)
        self.btn.clicked.connect(lambda :self.test_update(1.3))
        self.btn2.clicked.connect(lambda :self.test_update(0.8))

        # self.ani = Animation(self)

    def test_update(self,v):
        rrent = self.painter.virtualObj("rrent")
        rrent.scale(v)

        # rrent.move(200,200)

        # print(rrent.type())
        # print(rrent.getVirtualObjectAttr())
        # # rrent.updateArgs(50,50,100,100,3,3)
        # # rrent.updateArgs(50,50,100,100)
        # rrent.updateOpenAttr(openAttr={"color":"red"})
        # rrent.updateBrushAttr(brushAttr={"color":"blue"})
        self.update()

    def paintEvent(self, e:QPaintEvent) -> None:
        self.painter.begin(self)
        self.painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)
        # self.painter.drawRoundedRect(50,50,50,50,5,5,virtualObjectName="rrent")
        self.painter.drawRect(50,50,50,50,virtualObjectName="rrent")

        self.painter.end()

'''
    修复说明
    重新优化结构,将虚拟对象图形类,拆分为(虚拟对象图形管理类,虚拟对象图形类)
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()

    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
