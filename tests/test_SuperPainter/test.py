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


        self.btn = QPushButton(self)
        self.btn.setText("按钮")
        self.btn.clicked.connect(self.test)


    def test(self):
        rent = self.painter.virtualObj("rrent")
        print(rent)
        if rent.isHide():
            rent.setHide(False)
        else:
            rent.setHide(True)
        self.update()

    def paintEvent(self, e:QPaintEvent) -> None:
        self.painter.begin(self)
        self.painter.setRenderHints(qt.Antialiasing | qt.SmoothPixmapTransform | qt.TextAntialiasing)

        self.painter.drawRect(50,0,50,self.height(),virtualObjectName="rrent",brushAttr={"c":"green"})


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
