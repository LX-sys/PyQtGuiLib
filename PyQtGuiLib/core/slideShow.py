# -*- coding:utf-8 -*-
# @time:2023/1/10 12:41
# @author:LX
# @file:SlideShow.py
# @software:PyCharm

from PyQtGuiLib.header import (
    QWidget,
    QPushButton,
    QPoint,
    QPropertyAnimation,
    Signal
)

from PyQtGuiLib.styles import ButtonStyle

'''
    组件轮播
'''
class SlideShow(QWidget):
    # 切换窗口事件
    changeWidget = Signal(QWidget)

    # 动画的方向模式
    Ani_Left = "left"
    Ani_Right = "right"
    Ani_Down = "down"
    Ani_Up = "up"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(700, 300)
        #
        self.widgets = []

        self.animation_time = 1000 # 毫秒

        # 动画运行方向,当前动作
        self.ani_direction = (SlideShow.Ani_Left, SlideShow.Ani_Right)

        # 设置自动轮播,自动轮播的方向
        self.is_auto_slide = False
        self.auto_ani_direction = "R"

        # 窗口索引
        self.index = 0

        # 创建两侧按钮
        self.createButtons()

    # 设置自动轮播
    def setAutoSlideShow(self,b:bool,interval=1500,direction_:str="R"):
        if direction_ not in ["R","L"]:
            raise TypeError("Parameter error, Support only 'R' or 'L' !")

        if interval <= self.animation_time:
            raise ValueError("The interval between auto wheel casting must be longer than the animation time!")

        self.is_auto_slide = b
        self.startTimer(interval)
        self.auto_ani_direction = direction_


    # 左上方向
    def lu_direction(self) -> str:
        return self.ani_direction[0]

    # 右下方向
    def rd_direction(self) -> str:
        return self.ani_direction[1]

    # 创建两侧按钮
    def createButtons(self):
        # 左右按钮
        self.Ani_Left_btn = QPushButton("左",self)
        self.Ani_Right_btn = QPushButton("右",self)
        self.Ani_Left_btn.setObjectName("Ani_Left_btn")
        self.Ani_Right_btn.setObjectName("Ani_Right_btn")
        self.Ani_Left_btn.resize(50,50)
        self.Ani_Right_btn.resize(50,50)
        self.Ani_Left_btn.clicked.connect(lambda :self.moveWidget("L"))
        self.Ani_Right_btn.clicked.connect(lambda :self.moveWidget("R"))
        self.btnStyle()
        self.btnPos()

    # 按钮样式
    def btnStyle(self):
        self.Ani_Left_btn.setStyleSheet('''
#Ani_Left_btn{
background-color:transparent;
border:2px solid #73ffcc;
color:#73ffcc;
border-radius:5px;
}
#Ani_Left_btn:hover{
border:2px solid #00557f;
}
        ''')
        self.Ani_Right_btn.setStyleSheet('''
#Ani_Right_btn{
background-color:transparent;
border:2px solid #73ffcc;
color:#73ffcc;
border-radius:5px;
}
#Ani_Right_btn:hover{
border:2px solid #00557f;
}
                ''')

    def btnPos(self):
        self.Ani_Left_btn.move(5, self.height() // 2 - self.Ani_Left_btn.height() // 2)
        self.Ani_Right_btn.move(self.width() - self.Ani_Right_btn.width() - 5,
                            self.height() // 2 - self.Ani_Left_btn.height() // 2)

    def count(self) -> int:
        return len(self.widgets)

    # 移动窗口
    def moveWidget(self,direction_:str):

        direction = None

        w_1 = self.widgets[self.index]
        if direction_ == "R": # self.index < self.count() - 1
            direction = self.rd_direction()
            self.index += 1
            if self.index > self.count()-1:
                self.index = 0

        if direction_ == "L": # and self.index >= 0
            direction = self.lu_direction()
            self.index -= 1
            if self.index < -self.count():
                self.index = -1

        if not direction:
            return

        w_2 = self.widgets[self.index]
        self.changeWidget.emit(w_2)# 切换窗口时发送信号
        w_1.show()
        w_2.show()

        # 隐藏其他窗口
        for w in self.widgets:
            if w != w_1 and w != w_2:
                w.hide()

        self.ani_(w_1, w_2, direction)

    def addWidget(self,widget:QWidget):
        widget.setParent(self)
        widget.resize(self.size())
        widget.lower()
        self.widgets.append(widget)

        if self.count() > 1:
            widget.hide()

    # 设置动作模式
    def setAinDirectionMode(self, mode:tuple):
        if mode[0] not in [SlideShow.Ani_Up,SlideShow.Ani_Left] and\
            mode[1] not in [SlideShow.Ani_Right,SlideShow.Ani_Down]:
            raise TypeError("Parameter error!")

        self.ani_direction = mode

    # 设置按钮的隐藏和显示
    def setButtonsHide(self,b:bool):
        self.Ani_Left_btn.setHidden(b)
        self.Ani_Right_btn.setHidden(b)

    def aniDirection(self) -> tuple:
        return self.ani_direction

    # 移除窗口(只会移除,不会消毁)
    def removeWidget(self,widget:QWidget):
        self.widgets.remove(widget)

    # 切换到指定窗口
    def setCurrentIndex(self,index:int=0):
        n = 0
        direction = "R"
        if index > self.index:
            n = index - self.index

        if index < self.index:
            direction = "L"
            n = self.index - index

        for _ in range(abs(n)):
            self.moveWidget(direction)


    def ani_(self,widget_out:QWidget,widget_show:QWidget,direction:str):
        '''
            widget_out:被移走的窗口
            widget_show:准备显示的窗口
        '''

        if not widget_out.parent():
            widget_out.setParent(self)

        if not widget_show.parent():
            widget_show.setParent(self)

        wid1,wid2 = widget_out,widget_show
        wid1.resize(self.size())
        wid2.resize(self.size())

        ani_1 = QPropertyAnimation(wid1,b"pos",self)
        ani_2 = QPropertyAnimation(wid2,b"pos",self)
        ani_1.setDuration(self.animation_time)
        ani_2.setDuration(self.animation_time)

        if direction == SlideShow.Ani_Left:
            s_ani_1, e_ani_1 = QPoint(0, 0), QPoint(-self.width(), 0)
            s_ani_2, e_ani_2 = QPoint(self.width(), 0), QPoint(0, 0)
        elif direction == SlideShow.Ani_Up:
            s_ani_1, e_ani_1 = QPoint(0, 0), QPoint(0, -self.height())
            s_ani_2, e_ani_2 = QPoint(0, self.height()), QPoint(0, 0)
        elif direction == SlideShow.Ani_Down:
            s_ani_1, e_ani_1 = QPoint(0, 0), QPoint(0, self.height())
            s_ani_2, e_ani_2 = QPoint(0, -self.height()), QPoint(0, 0)
        else:
            s_ani_1,e_ani_1 = QPoint(0,0),QPoint(self.width(),0)
            s_ani_2,e_ani_2 = QPoint(-self.width(),0),QPoint(0,0)

        ani_1.setStartValue(s_ani_1)
        ani_1.setEndValue(e_ani_1)

        ani_2.setStartValue(s_ani_2)
        ani_2.setEndValue(e_ani_2)

        ani_1.start()
        ani_2.start()

    # 通过索引获取窗口
    def getWidget(self,index:int) -> QWidget:
        return self.widgets[index]

    # 反按钮对象
    def getButtons(self)->tuple:
        return self.Ani_Left_btn,self.Ani_Right_btn

    def isEmpty(self) -> bool:
        return True if not self.widgets else False

    def timerEvent(self, event) -> None:
        if self.is_auto_slide:
            self.moveWidget(self.auto_ani_direction)

    def resizeEvent(self, event) -> None:
        self.btnPos()
        super().resizeEvent(event)
