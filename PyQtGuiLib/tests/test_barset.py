# -*- coding:utf-8 -*-
# @time:2022/12/2316:33
# @author:LX
# @file:test_barset.py
# @software:PyCharm

'''

    进度条集合测试
'''

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QMainWindow,
    QThread,
    Signal,
    QColor,
    QSlider
)

from PyQtGuiLib.core.progressBar import WaterBar
from PyQtGuiLib.core.progressBar import CircularBar
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

        self.setObjectName("test")
#         self.setStyleSheet('''
# #test{
# background-color: rgb(0, 0, 0);
# }
#         ''')

        self.waterbar = WaterBar(self)
        self.waterbar.move(100,250)

        # 加载进度条
        self.loadbar = LoadBar(self)
        self.loadbar.move(250,100)
        self.loadbar.resize(350,45)


        # 圆环进度条
        self.cir = CircularBar(self)
        self.cir.resize(120, 120)
        self.cir.setVariableLineSegment(CircularBar.Double)
        self.cir.setOuterStyle(CircularBar.CustomDashLine)
        self.cir.setOuterDashPattern([2, 3, 5, 6])
        self.cir.setInnerStyle(CircularBar.DashLine)
        self.cir.setTextSize(15)
        self.cir.move(50, 50)

        self.th = DurationTimeThread()
        self.th.added.connect(self.test)
        self.th.start()


    def test(self, n):
        self.cir.setValue(n)
        self.loadbar.setValue(n)
        self.waterbar.setValue(n)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestPullOverWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())