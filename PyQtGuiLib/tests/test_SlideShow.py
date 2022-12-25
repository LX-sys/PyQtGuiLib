# -*- coding:utf-8 -*-
# @time:2022/12/259:42
# @author:LX
# @file:test_SlideShow.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget
)

from PyQtGuiLib.core import SlideShow


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(1000,600)

        self.ss = SlideShow(self)
        # self.ss.setMode(SlideShow.CardMode)
        self.ss.move(50,50)
        self.ss.resize(600,300)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())