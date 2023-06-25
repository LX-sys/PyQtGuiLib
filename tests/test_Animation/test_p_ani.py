# -*- coding:utf-8 -*-
# @time:2023/6/2517:32
# @author:LX
# @file:test_p_ani.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QPoint,
    QPushButton,
    QSpinBox,
    QRect,
    QObject
)

from PyQtGuiLib.animation import Animation
from PyQtGuiLib.styles import SuperPainter

'''
    SuperPainter + Animation 实现图形动画
'''

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,600)

        self.painter = SuperPainter(self)

        self.btn = QPushButton(self)
        self.btn.setText("执行painter动画")
        self.btn.clicked.connect(self.test_ani)

    def test_ani(self):
        vobj = self.painter.virtualObj("arect")
        self.ani = Animation()
        self.ani.addAni(QPoint(*vobj.getPos()),QPoint(100,100),courseFunc=self.updateRect)
        self.ani.start()

    def updateRect(self,pos:QPoint):
        vobj = self.painter.virtualObj("arect")
        vobj.updateIndexToArgs(2,pos.x())
        vobj.updateIndexToArgs(3,pos.y())
        self.update()

    def paintEvent(self, e):
        self.painter.begin(self)
        self.painter.drawRect(50,50,50,50,virtualObjectName="arect")
        self.painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())