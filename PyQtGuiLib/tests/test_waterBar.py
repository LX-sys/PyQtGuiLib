# -*- coding:utf-8 -*-
# @time:2022/12/2217:18
# @author:LX
# @file:test_waterBar.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    QApplication,
    QMainWindow,
    QThread,
    Signal,
    QColor,
    QSlider,
)

from PyQtGuiLib.core.progressBar import WaterBar

class DurationTimeThread(QThread):
    added = Signal(int)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def run(self) -> None:
        n=1
        while True:
            self.added.emit(n)
            n += 1
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
        self.waterbar.resize(120,120)
        self.waterbar.setTextSize(30)
        self.waterbar.move(50,100)

        self.th = DurationTimeThread()
        self.th.added.connect(self.test1)
        self.th.start()

    def test1(self,v):
        self.waterbar.setValue(v)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestPullOverWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())