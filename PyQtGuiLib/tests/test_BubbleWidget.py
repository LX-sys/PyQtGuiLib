# -*- coding:utf-8 -*-
# @time:2022/12/1018:13
# @author:LX
# @file:test_BubbleWidget.py
# @software:PyCharm

from PyQtGuiLib.header import PYQT_VERSIONS
from PyQtGuiLib.header import (
    sys,
    QApplication,
    QWidget,
    QPushButton,
)

from PyQtGuiLib.core import BubbleWidget

'''
    气泡窗口的测试用例
'''

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        self.setWindowOpacity(0.5)


        self.btn = QPushButton("一号玩家",self)
        self.btn.resize(130,100)
        self.btn.move(200,200)

        # 气泡控件
        self.bu = BubbleWidget(self)
        self.bu.resize(150,100)
        self.bu.setDirection(BubbleWidget.Top)
        self.bu.setDurationTime(BubbleWidget.Be_Forever)
        self.bu.setAnimationEnabled(True)
        self.bu.setTrack(self.btn)
        self.bu.setText("你好世界")
        # self.bu.setText("hello world")

        self.bu.finished.connect(lambda :print("111111111"))
        # self.bu.move(80,100) # 如果不想手动设置位置可以用下面控件追踪功能

        # # --------
        # self.btn2 = QPushButton("二号玩家",self)
        # self.btn2.resize(150,80)
        # self.btn2.move(400,350)
        #
        # self.bu2 = BubbleWidget(self)
        # self.bu2.setText("你才是哼")
        # # 反向的设置一定要在追踪前面
        # self.bu2.setDurationTime(BubbleWidget.Be_Forever)
        # self.bu2.setDirection(BubbleWidget.Left)
        # self.bu2.setTrack(self.btn2)
        # self.bu2.setTextColor(QColor(255, 255, 0))
        # self.bu2.setBColor(QColor(170, 0, 255))
        # # self.bu2.setKm(30,10)
        # self.bu2.resize(260,80)
        #
        # self.bu3 = BubbleWidget(self)
        # self.bu3.setText("绿色")
        # self.bu3.setDirection(BubbleWidget.NoNone)
        # self.bu3.setBColor(QColor(170, 255, 127))
        # self.bu3.move(80,300)
        # self.bu3.setKm(80,25)
        # self.bu3.resize(160,80)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())