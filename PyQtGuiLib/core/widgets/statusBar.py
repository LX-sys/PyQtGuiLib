# -*- coding:utf-8 -*-
# @time:2023/1/411:16
# @author:LX
# @file:statusBar.py
# @software:PyCharm

from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    sys,
    time,
    QApplication,
    QWidget,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFont,
    QFontMetricsF,
    QSpacerItem,
    QSizePolicy,
)
'''
    状态栏
'''

class StatusBar(QFrame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.h = 30

        self.__parent = None #  type:QWidget

        if args:
            self.__parent = args[0]

        # 本地时间
        self.format = "%Y-%m-%d %H:%M:%S"
        self.local_time = time.strftime(self.format, time.localtime())
        self.l_time = QLabel(self.local_time)

        self.__hlay = QHBoxLayout(self)
        self.__hlay.setContentsMargins(6,0,6,0)
        self.__hlay.setSpacing(6)

        self.hSpacer = QSpacerItem(704, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.updateStatusSize()

        self.startTimer(1000)

    def setParent(self, parent:QWidget) -> None:
        self.__parent = parent
        super().setParent(parent)

        if self.__parent is not None:
            self.move(0,self.__parent.height()-self.h)
            self.resize(self.__parent.width(),self.h)

    def __addSpacer(self):
        self.__hlay.addItem(self.hSpacer)
        self.__hlay.removeItem(self.hSpacer)
        self.__hlay.addItem(self.hSpacer)

    # 添加文本
    def addText(self,text:str,style:str=None):
        l = QLabel(text)
        if style:
            l.setStyleSheet(style)
        self.__hlay.addWidget(l)
        self.__addSpacer()

    # 添加按钮
    def addButton(self,text:str,style:str=None):
        btn = QPushButton(text)
        if style:
            btn.setStyleSheet(style)
        self.__hlay.addWidget(btn)
        self.__addSpacer()

    # 添加widget
    def addWidget(self,widget:QWidget,style:str=None):
        if style:
            widget.setStyleSheet(style)
        self.__hlay.addWidget(widget)
        self.__addSpacer()

    # 添加时间
    def addTime(self,style:str=None):
        if style:
            self.l_time.setStyleSheet(style)
        self.__hlay.addWidget(self.l_time)
        self.__addSpacer()

    def updateStatusSize(self):
        self.move(0, self.__parent.height() - self.h)
        self.resize(self.__parent.width(), self.h)

    def timerEvent(self,e) -> None:
        self.local_time = time.strftime(self.format, time.localtime())
        self.l_time.setText(self.local_time)