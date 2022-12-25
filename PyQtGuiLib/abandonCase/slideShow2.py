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
    QSize
)



'''
    弃案
    轮播图功能
        风格: 扁平,卡片
'''
class SlideShow(QWidget):
    # 扁平/卡片 风格
    FlatMode = "flat"  # 经典
    CardMode = "card"  # 卡片

    # 方向
    Left = "left"
    Right = "right"

    # 动画
    Translation = "translation"  # 平移
    FadeOut = "fadeout" # 渐隐渐显

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(700, 300)

        self.show_mode = SlideShow.FlatMode # 展示模式
        self.animation_mode = SlideShow.Translation  # 动画模式

        self.index = 0  # 索引

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

            if direction == SlideShow.Left:
                self.index -= 1
                if self.index < 0:
                    self.index = widgets_count - 1
            if direction == SlideShow.Right:
                self.index += 1
                if self.index > widgets_count - 1:
                    self.index = 0
            self.hideCurrentWidgets()
            self.show_()

        if self.show_mode == SlideShow.CardMode:  # 卡片模式
            widgets_count = len(self.widgets)

            if widgets_count >= 2:
                if direction == SlideShow.Left:
                    pass
                if direction == SlideShow.Right:
                    pass

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
        # 隐藏清除
        self.hideCurrentWidgets()
        self.current_widgets.clear()

        if self.show_mode == SlideShow.FlatMode:  # 经典模式
            # 优先展示第一个窗口
            widget = self.widgets[self.index]  # type:QWidget
            widget.setParent(self)
            widget.show()
            widget.lower()
            widget.resize(self.width(),self.height())

            # 添加到当前展示的窗口
            self.current_widgets.append(widget)

        # -----------------------------------------------
        if self.show_mode == SlideShow.CardMode:  # 卡片模式
            '''
                展示窗口的时候
                    如果只有一个窗口,那直接居中展示
                    两个窗口时,一个左边,一个居中
                    三个窗口时,一个左边一个居中一个右边
                    更多窗口时,优先展示前三个
            '''
            widgets_count = len(self.widgets)
            if not widgets_count:
                return

            # 每个轮播窗口的大小
            size = QSize(self.width() // 2, self.height() // 2)

            if widgets_count == 1:
                widget = self.widgets[0] # type:QWidget
                self.current_widgets.append(widget)
                # 居中
                center_pos = QPoint(self.width() // 2 - widget.width() // 2,
                                    self.height() // 2 - widget.height() // 2)
                self.__createWidget(widget,size,center_pos)
            elif widgets_count == 2:
                left_widget,widget = self.widgets
                self.current_widgets.extend(self.widgets)

                # 居中
                center_pos = QPoint(self.width() // 2 - widget.width() // 2,
                                    self.height() // 2 - widget.height() // 2)
                # 左边轮播图的位置
                left_pos = QPoint(center_pos.x() - self.width()//5,
                                  center_pos.y())

                left_size = QSize(self.width()//4,self.height()//2)
                center_size = QSize(self.width()//3,self.height()//2)
                self.__createWidget(left_widget, left_size, left_pos)
                self.__createWidget(widget, center_size, center_pos)
            elif widgets_count >= 3:
                left_widget, widget,right_widget = self.widgets[:3]
                self.current_widgets.extend(self.widgets[:3])

                # 居中
                center_pos = QPoint(self.width() // 2 - widget.width() // 2,
                                    self.height() // 2 - widget.height() // 2)
                # 左边轮播图的位置
                left_pos = QPoint(center_pos.x() - self.width() // 5,
                                  center_pos.y())

                # 右边轮播图的位置
                right_pos = QPoint(center_pos.x() + self.width() // 4,
                                  center_pos.y())

                left_size = QSize(self.width() // 4, self.height() // 2)
                right_size = left_size
                center_size = QSize(self.width() // 3, self.height() // 2)
                self.__createWidget(left_widget, left_size, left_pos)
                self.__createWidget(right_widget, right_size, right_pos)
                self.__createWidget(widget, center_size, center_pos)

    # 创建窗口
    def __createWidget(self,widget:QWidget,size:QSize,point:QPoint):
        widget.setParent(self)
        widget.resize(size)
        widget.raise_()
        widget.move(point)
        widget.show()

    # 动画
    def animation_(self):
        if self.animation_mode == SlideShow.Translation:
            pass
        
        if self.animation_mode == SlideShow.FlatMode:
            pass

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