# -*- coding:utf-8 -*-
# @time:2022/12/2317:54
# @author:LX
# @file:SlideShow.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QResizeEvent,
    QPushButton,
    QStackedWidget,
    QMouseEvent
)


'''

    轮播图功能
        风格: 扁平,卡片
'''

class SlideShow(QWidget):
    # 扁平/卡片 风格
    FlatMode = "flat"
    CardMode = "card"

    # 方向
    Left = "left"
    Right = "right"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(700, 300)

        # 展示模式
        self.mode = SlideShow.CardMode

        self.index = 0 # 索引

        # 设置是否自动轮播
        self.is_auto_carousel = False
        self.directionFun = None # 方向函数

        if self.mode == SlideShow.FlatMode:
            self.__core_widget = QStackedWidget(self)
            self.__core_widget.lower() # 窗口放置在底层
            self.__core_widget.setStyleSheet("border:1px solid red;")
        self.widgets = [] # 窗口列表

        # 左右按钮
        self.__left_btn = QPushButton("左",self)
        self.__right_btn = QPushButton("右",self)
        self.__left_btn.resize(50,50)
        self.__right_btn.resize(50,50)

        # 切换窗口
        self.__left_btn.clicked.connect(lambda :self.roll_event(SlideShow.Left))
        self.__right_btn.clicked.connect(lambda :self.roll_event(SlideShow.Right))

        t = QWidget()
        t.setStyleSheet("background-color:red;")
        t1 = QWidget()
        t1.setStyleSheet("background-color:blue;")
        t2 = QWidget()
        t2.setStyleSheet("background-color:green;")
        self.addWidget(t)
        # self.addWidget(t1)
        # self.addWidget(t2)

        # self.setAutoCarousel(True,1000,SlideShow.Left)
        # 鼠标跟踪
        # self.setMouseTracking(True)

    # 轮动事件
    def roll_event(self,direction:str):
        if direction == SlideShow.Right:
            self.index += 1
            if self.index > len(self.widgets) - 1:
                self.index = 0
        elif direction == SlideShow.Left:
            self.index -= 1
            if self.index < 0:
                self.index = len(self.widgets) - 1

        if self.mode == SlideShow.FlatMode:
            self.__core_widget.setCurrentIndex(self.index)


    # 设置展示模式
    def setMode(self,mode:str):
        self.mode = mode

    # 设置自动轮播
    def setAutoCarousel(self,b:bool,interval:int=2000,direction:str="right"):
        self.is_auto_carousel = True
        self.startTimer(interval)
        if direction == SlideShow.Left:
            self.directionFun = self.up
        elif direction == SlideShow.Right:
            self.directionFun = self.next

        # 禁止/解放
        self.__left_btn.setEnabled(not b)
        self.__right_btn.setEnabled(not b)

    # 添加窗口
    def addWidget(self,widget:QWidget):
        if self.mode == SlideShow.FlatMode:
            self.__core_widget.addWidget(widget)
        self.widgets.append(widget)

    def getWidgets(self)->list:
        return self.widgets

    def __pos(self):
        self.__left_btn.move(5,self.height()//2-self.__left_btn.height()//2)
        self.__right_btn.move(self.width()-self.__right_btn.width()-5,
                              self.height()//2-self.__left_btn.height()//2)
        if self.mode == SlideShow.FlatMode:
            self.__core_widget.resize(self.size())

        if self.mode == SlideShow.CardMode:
            if len(self.widgets) == 1:
                self.widgets[0].setParent(self)
                self.widgets[0].move(self.width()//2-self.widgets[0].width()//2,
                                     self.height()//2-self.widgets[0].height()//2)
                self.widgets[0].resize(self.width()//2,self.height()//2)


    def resizeEvent(self, e: QResizeEvent) -> None:
        self.__pos()
        super().resizeEvent(e)

    def timerEvent(self, e) -> None:
        if self.is_auto_carousel and self.directionFun:
            self.directionFun()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SlideShow()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())