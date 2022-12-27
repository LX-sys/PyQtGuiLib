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
    Qt,
    QHBoxLayout,
)

from PyQtGuiLib.core import SlideShow


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(1000,600)

        self.flag = True

        # 窗口轮播功能
        self.ss = SlideShow(self)
        # self.ss.setAinDirectionMode((SlideShow.Ani_Up,SlideShow.Ani_Down))
        self.ss.setAutoSlideShow(True,direction=SlideShow.Ani_Down,is_not_show_btn=False)
        # self.ss.setHideButtons(True)
        self.ss.move(50,50)
        self.ss.resize(600,200)
        self.test()  # 添加测试窗口

        self.ss.switchWidgeted.connect(self.my_event)

    def my_event(self,index:int):
        print("当前索引:",index)
        # if self.flag:
        #     self.ss.removeWidget(2)
        #     self.flag = False

    def test(self):
        t = QWidget()
        tl = QLabel("1")
        tl.setAlignment(Qt.AlignCenter)
        lh = QHBoxLayout(t)
        lh.addWidget(tl)
        tl.setStyleSheet('font: 60pt "微软雅黑";')
        t.setStyleSheet("background-color:#00aa7f;")
        t2 = QWidget()
        tl2 = QLabel("2")
        tl2.setAlignment(Qt.AlignCenter)
        lh2 = QHBoxLayout(t2)
        lh2.addWidget(tl2)
        tl2.setStyleSheet('font: 60pt "微软雅黑";')
        t2.setStyleSheet("background-color:#aaaaff;")
        t3 = QWidget()
        tl3 = QLabel("3", t3)
        tl3.setAlignment(Qt.AlignCenter)
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

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())