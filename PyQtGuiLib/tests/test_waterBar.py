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
    Qt
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
            n+=1
            self.msleep(100)
            if n == 360+1:
                print("完成")
                break

class TestPullOverWidget(QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        self.setObjectName("test")
        self.setStyleSheet('''
#test{
background-color: rgb(0, 0, 0);
}
        ''')

        self.waterbar = WaterBar(self)
        self.waterbar.move(50,100)


        self.ss = QSlider(self)
        self.ss.setMinimum(0)
        self.ss.setMaximum(360)
        self.ss.setOrientation(Qt.Horizontal)
        self.ss.move(50,350)

        self.se = QSlider(self)
        self.se.setMinimum(0)
        self.se.setMaximum(360)
        self.se.setOrientation(Qt.Horizontal)
        self.se.move(250,350)

        self.ss.valueChanged.connect(self.test1)
        self.se.valueChanged.connect(self.test2)
        # self.th = DurationTimeThread()
        # self.th.added.connect(self.test)
        # self.th.start()

    def test1(self,v):
        self.waterbar.sn = v
        self.waterbar.update()
    def test2(self,v):
        self.waterbar.en = v
        self.waterbar.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TestPullOverWidget()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
