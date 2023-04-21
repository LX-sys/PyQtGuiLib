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
    QRect,
    QPoint,
    QLine
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
        self.update()

    def paintEvent(self, e:QPaintEvent) -> None:
        self.painter.begin(self)
        self.painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        # self.painter.drawRect(self.width()//2-25,self.height()//2-25, 50, 50,openAttr={"c":"red"})
        # self.painter.translate(self.width()//2-25,self.height()//2-25)
        # self.painter.rotate(60)
        # self.painter.shear(0.2,0.5)

        self.painter.drawRect(50,50,50,50,virtualObjectName="rrent",brushAttr={"c":"green"})
        self.painter.setCompositionMode(QPainter.CompositionMode_Xor)
        self.painter.drawRect(50,75,50,50,brushAttr={"c":"red"})
        # # self.painter.drawLines([QLine(10,10,100,100),QLine(50,50,100,100)],openAttr={"c":"red"})




        # op = QPen()
        # op.setColor(QColor(0,255,0))
        # op.setWidth(3)
        # self.painter.setPen(op)
        # self.painter.drawRect(50,50,100,100)
        # self.painter.save()
        #
        # self.painter.setPen(QColor(0, 0, 255))
        # self.painter.drawRect(200, 50, 50, 50)
        # self.painter.restore()
        #
        # self.painter.drawRect(200, 150, 50, 50)

        self.painter.end()


'''

'''

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()

    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
