# -*- coding:utf-8 -*-
# @time:2022/12/259:42
# @author:LX
# @file:test_SlideShow.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QLabel,
    qt,
    QHBoxLayout,
)

from PyQtGuiLib.core import SlideShow

'''
    窗口轮播功能
'''
class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(1000,600)

        self.flag = True

        # 窗口轮播功能
        self.ss = SlideShow(self)
        # self.ss.setButtonsHide(True)
        self.ss.move(50,50)
        self.ss.resize(600,200)
        self.test()  # 添加测试窗口

        self.ss.changeWidget.connect(self.my_event)

    def my_event(self,widget:QWidget):
        print("当前窗口:",widget)
        # if self.flag:
        #     self.ss.removeWidget(2)
        #     self.flag = False

    def test(self):
        t = QWidget()
        tl = QLabel("1")
        tl.setAlignment(qt.AlignCenter)
        lh = QHBoxLayout(t)
        lh.addWidget(tl)
        tl.setStyleSheet('font: 60pt "微软雅黑";')
        t.setStyleSheet("background-color:#00aa7f;")
        t2 = QWidget()
        tl2 = QLabel("2")
        tl2.setAlignment(qt.AlignCenter)
        lh2 = QHBoxLayout(t2)
        lh2.addWidget(tl2)
        tl2.setStyleSheet('font: 60pt "微软雅黑";')
        t2.setStyleSheet("background-color:#aaaaff;")
        t3 = QWidget()
        tl3 = QLabel("3", t3)
        tl3.setAlignment(qt.AlignCenter)
        lh3 = QHBoxLayout(t3)
        lh3.addWidget(tl3)
        tl3.setStyleSheet('font: 60pt "微软雅黑";')
        t3.setStyleSheet("background-color:green;")
        self.ss.addWidget(t)
        self.ss.addWidget(t2)
        self.ss.addWidget(t3)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6", "PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())