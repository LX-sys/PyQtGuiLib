# -*- coding:utf-8 -*-
# @time:2022/12/2215:14
# @author:LX
# @file:test_loadbar.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QMainWindow,
    QThread,
    Signal,
    QColor
)

from PyQtGuiLib.core.progressBar import LoadBar


class DurationTimeThread(QThread):
    added = Signal(int)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def run(self) -> None:
        n=1
        while True:
            self.added.emit(n)
            n+=1
            self.msleep(100)
            if n == 100+1:
                print("完成")
                break

class TestPullOverWidget(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        self.loadbar = LoadBar(self)
        self.loadbar.move(50,100)
        self.loadbar.resize(350,45)
        self.loadbar.setValue(0)

        self.th = DurationTimeThread()
        self.th.added.connect(self.test)
        self.th.start()

    def test(self,v):
        print(v)
        self.loadbar.setValue(v)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestPullOverWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())