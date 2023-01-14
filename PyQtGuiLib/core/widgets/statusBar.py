# -*- coding:utf-8 -*-
# @time:2023/1/411:16
# @author:LX
# @file:statusBar.py
# @software:PyCharm

from PyQtGuiLib.header import (
    is_win_sys,
    is_mac_sys,
    time,
    QThread,
    Signal,
    QWidget,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QPainter,
    QPaintEvent,
    QStyleOption,
    QStyle,
    qt
)
'''
    状态栏
'''


# 倒计时类
class CountDownThread(QThread):
    # 计时完成信号
    timeOuted = Signal()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.time_ = 0

    # 设置时间
    def setTime(self,time:int):
        self.time_ = time

    def run(self) -> None:
        while self.time_:
            self.sleep(1)
            self.time_-=1
        self.timeOuted.emit()


class StatusBar(QWidget):

    PosBottom = "PosBottom"
    PosTop = "PosTop"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.setAttribute(qt.WA_StyledBackground,True)

        self.h = 30

        self.__parent = None #  type:QWidget

        if args:
            self.__parent = args[0]

        # 本地时间
        self.format = "%Y-%m-%d %H:%M:%S"
        self.local_time = time.strftime(self.format, time.localtime())
        self.l_time = QLabel(self.local_time)

        # 状态栏位置
        self.status_pos = StatusBar.PosBottom

        # 创建倒计时类
        self.cd = CountDownThread()

        self.__hlay = QHBoxLayout(self)
        self.__hlay.setContentsMargins(6,0,6,0)
        if is_win_sys:
            self.__hlay.setSpacing(6)
        if is_mac_sys:
            self.__hlay.setSpacing(6*3)

        self.hSpacer = QSpacerItem(704, 20, qt.PolicyExpanding, qt.PolicyMinimum)

        self.defaultStyle()

        self.updateStatusSize()

        self.startTimer(1000)

    def defaultStyle(self):
        self.setStyleSheet("background-color: rgb(193, 193, 193);")

    # 设置时间格式
    def setTimeFormat(self,format:str="%Y-%m-%d %H:%M:%S"):
        self.format = format

    def setParent(self, parent:QWidget) -> None:
        self.__parent = parent
        super().setParent(parent)

        if self.__parent is not None:
            self.move(0,self.__parent.height()-self.h)
            self.resize(self.__parent.width(),self.h)

    # 设置状态栏位置
    def setStatusPos(self,mode:str):
        self.status_pos = mode

    def __addSpacer(self):
        self.__hlay.addItem(self.hSpacer)
        self.__hlay.removeItem(self.hSpacer)
        self.__hlay.addItem(self.hSpacer)

    # 添加文本
    def addText(self,text:str,style:str=None,duration:int=0):
        '''
            text:文本
            style:样式
            duration:持续时间后消失
        '''
        l = QLabel(text)
        if style:
            l.setStyleSheet(style)

        self.__hlay.addWidget(l)
        self.__addSpacer()

        # 移除布局
        def _del():
            self.__hlay.removeWidget(l)
            l.deleteLater()  # 销毁自己

        if duration > 0:
            self.cd.setTime(duration)
            self.cd.timeOuted.connect(lambda :_del())
            self.cd.start()

    # 添加按钮
    def addButton(self,text:str,style:str=None,callback=None):
        btn = QPushButton(text)
        if style:
            btn.setStyleSheet(style)
        if callback:
            btn.clicked.connect(callback)
        self.__hlay.addWidget(btn)
        self.__addSpacer()

    # 添加widget
    def addWidget(self,widget:QWidget,style:str=None):
        if style:
            widget.setStyleSheet(style)
        self.__hlay.addWidget(widget)
        self.__addSpacer()

    # 添加时间
    def addTime(self,style:str="background-color:transparent"):
        if style:
            self.l_time.setStyleSheet(style)
        self.__hlay.addWidget(self.l_time)
        self.__addSpacer()

    def updateStatusSize(self):
        if self.status_pos == StatusBar.PosTop:
            self.move(0, 0)
            self.resize(self.__parent.width(), self.h)
        elif self.status_pos == StatusBar.PosBottom:
            self.move(0, self.__parent.height() - self.h)
            self.resize(self.__parent.width(), self.h)

    def timerEvent(self,e) -> None:
        self.local_time = time.strftime(self.format, time.localtime())
        self.l_time.setText(self.local_time)

    def paintEvent(self, e: QPaintEvent) -> None:
        self.updateStatusSize()
        super().paintEvent(e)
