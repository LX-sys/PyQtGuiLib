# -*- coding:utf-8 -*-
# @time:2022/12/2710:59
# @author:LX
# @file:test_gradientBar.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QMainWindow,
    QThread,
    Signal,
    QColor,
    QThread
)

from PyQtGuiLib.core.progressBar import GradientBar


class DurationTimeThread(QThread):
    added = Signal(int)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def run(self) -> None:
        n=1
        while True:
            self.added.emit(n)
            n+=1
            self.msleep(80)
            if n == 100+1:
                break

'''
    线性渐变进度条 测试用例
'''

class TestGradientBar(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        self.gbar = GradientBar(self)
        self.gbar.move(50,50)
        self.gbar.resize(500,10)
        self.gbar.setValue(0)
        self.gbar.setColorAts(
            [(0.2, QColor(170, 170, 255)), (0.4, QColor(170, 255, 127)), (0.6, QColor(85, 170, 127))]
        )
        # self.gbar.appendColor((0.5,QColor(85, 85, 127)))
        self.gbar.setRadius(3)

        self.th = DurationTimeThread()
        self.th.added.connect(self.test)
        self.th.start()

    def test(self,n):
        print(n)
        # if n > 20 and n <50:
        #     self.gbar.setRadius(2)
        # elif n>50:
        #     self.gbar.setRadius(5)
        self.gbar.setValue(n)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestGradientBar()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())