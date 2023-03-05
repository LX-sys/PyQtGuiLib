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
    QPushButton
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

        self.boyy = QHBoxLayout(self)

        # 窗口轮播功能
        self.ss = SlideShow()

        # self.ss.setAutoSlideShow(True)
        # self.ss.setButtonsHide(True)
        self.ss.move(50,50)
        # self.ss.resize(600,200)
        self.test()  # 添加测试窗口

        self.boyy.addWidget(self.ss)

        self.ss.changeWidget.connect(self.my_event)

    def my_event(self,index:int):
        print("当前索引:",index)

    def change(self):
        self.ss.removeWidget(self.ss.getWidget(1))

    def test(self):
        t = QWidget()
        tl = QLabel("1")
        tl.setAlignment(qt.AlignCenter)
        lh = QHBoxLayout(t)
        btn1 = QPushButton("删除")
        btn1.clicked.connect(self.change)
        lh.addWidget(tl)
        lh.addWidget(btn1)
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