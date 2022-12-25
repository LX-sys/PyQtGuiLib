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
    QMouseEvent,
    QPoint,
    QSize,
    QPropertyAnimation
)



'''

    轮播图功能
        风格: 扁平
'''
class SlideShow(QWidget):
    # 扁平 风格
    FlatMode = "flat"  # 经典
    # 方向
    Left = "left"
    Right = "right"

    # 动画
    Translation = "translation"  # 平移

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(700, 300)

        self.show_mode = SlideShow.FlatMode # 展示模式
        self.animation_mode = SlideShow.Translation  # 动画模式

        self.animation_time = 300 # 毫秒

        self.index = [-1,0]  # 索引

        # 左右按钮
        self.left_btn = QPushButton("左",self)
        self.right_btn = QPushButton("右",self)
        self.left_btn.setObjectName("left_btn")
        self.right_btn.setObjectName("right_btn")
        self.left_btn.resize(50,50)
        self.right_btn.resize(50,50)
        self.left_btn.clicked.connect(lambda :self.roll_event(SlideShow.Left))
        self.right_btn.clicked.connect(lambda :self.roll_event(SlideShow.Right))

        # 窗口
        self.widgets = []  # 所有已经添加的窗口
        self.current_widgets = [] # 当前已经展示出来的轮播窗口对象

        self.move_ani = QPropertyAnimation(self)
        self.move_ani.setPropertyName(b"pos")

        # 测试
        self.test()

    def test(self):
        t = QWidget()
        t.setStyleSheet("background-color:red;")
        t2 = QWidget()
        t2.setStyleSheet("background-color:blue;")
        t3 = QWidget()
        t3.setStyleSheet("background-color:green;")
        self.addWidget(t)
        self.addWidget(t2)
        self.addWidget(t3)

    # 返回当前窗口上已经展示的轮播对象窗口
    def currentWidgets(self) -> list:
        return self.current_widgets

    # 隐藏当前已经展示的轮播对象窗口
    def hideCurrentWidgets(self):
        for widget in self.currentWidgets():
            widget.hide()

    # 轮播事件
    def roll_event(self, direction: str):
        if self.show_mode == SlideShow.FlatMode:  # 经典模式
            widgets_count = len(self.widgets)

            self.index[0] += 1
            self.index[1] += 1

            if self.index[0] > widgets_count - 1:
                self.index[0] = 0

            if self.index[1] > widgets_count - 1:
                self.index[1] = 0

            self.rollShow(direction)

    # 滚动显示
    def rollShow(self,direction: str):
        widget = self.widgets[self.index[0]] # type:QWidget
        widget2 = self.widgets[self.index[1]] # type:QWidget
        self.__createWidget(widget2)
        self.animation_(direction,widget,widget2)

    def addWidget(self,widget:QWidget):
        self.widgets.append(widget)
        # 展示
        self.show_()

    # 两侧的按钮
    def btnPos(self):
        self.left_btn.move(5, self.height() // 2 - self.left_btn.height() // 2)
        self.right_btn.move(self.width() - self.right_btn.width() - 5,
                            self.height() // 2 - self.left_btn.height() // 2)

    # 展示
    def show_(self):
        if self.show_mode == SlideShow.FlatMode:  # 经典模式
            # 优先展示第一个窗口
            widget = self.widgets[0]  # type:QWidget
            self.__createWidget(widget)

    # 创建窗口
    def __createWidget(self,widget:QWidget):
        widget.setParent(self)
        widget.resize(QSize(self.width(),self.height()))
        widget.lower()
        widget.move(QPoint(0,0))
        widget.show()

    # 动画
    def animation_(self,direction:str,widget:QWidget,widget2:QWidget):
        if self.animation_mode == SlideShow.Translation:
            if len(self.widgets) >= 2:
                move_ani = QPropertyAnimation(self)
                move_ani2 = QPropertyAnimation(self)
                move_ani.setPropertyName(b"pos")
                move_ani2.setPropertyName(b"pos")
                move_ani.setTargetObject(widget)
                move_ani2.setTargetObject(widget2)

                move_ani.setStartValue(widget.pos())
                if direction == SlideShow.Right:
                    end_value = QPoint(widget.width(), 0)
                    start_value = QPoint(-widget.width(), 0)
                elif direction == SlideShow.Left:
                    end_value = QPoint(-widget.width(), 0)
                    start_value = QPoint(widget.width(), 0)
                move_ani.setEndValue(end_value)
                move_ani2.setStartValue(start_value)
                move_ani2.setEndValue(QPoint(0, 0))

                move_ani.setDuration(self.animation_time)
                move_ani2.setDuration(self.animation_time)
                move_ani.start()
                move_ani2.start()

    def resizeEvent(self, e:QResizeEvent) -> None:
        self.btnPos()
        self.show_()
        super().resizeEvent(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SlideShow()
    win.show()

    if PYQT_VERSIONS == "PyQt6":
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())