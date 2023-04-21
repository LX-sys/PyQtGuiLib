# -*- coding:utf-8 -*-
# @time:2023/4/2013:48
# @author:LX
# @file:drawer.py
# @software:PyCharm

from PyQtGuiLib.header import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    qt
)

from PyQtGuiLib.animation import Animation


class DrawerItem(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(300, 300)

        self.__vboy = QVBoxLayout(self)
        self.__vboy.setSpacing(0)
        self.__vboy.setContentsMargins(0,0,0,0)
        self.setFixedHeight(50)

        self._sp = QSpacerItem(0,0,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.__flag = False

        self.__duration = 200
        self.__area = 300

        self.setFixedHeight(30)

    def setFixedHeight(self, h: int) -> None:
        self._fh = h
        super().setFixedHeight(h)

    def setDuration(self,duration:int):
        self.__duration =duration

    # 设置展开高度
    def setDevelopedArea(self,area):
        self.__area = area

    def stretch_event(self):
        self.__ani = Animation()
        self.__ani.setStartMode(Animation.Parallel)
        if self.__flag is False:
            self.__ani.addAni(self.btn.height(),self.__area,duration=self.__duration,courseFunc=self.setFixedHeight)
            self.__ani.addAni(self.expansion_widget.height(),self.__area,duration=self.__duration,courseFunc=self.expansion_widget.setFixedHeight)
            self.__flag = True
        else:
            self.__ani.addAni(self.height(),self.btn.height(),duration=self.__duration,courseFunc=self.setFixedHeight)
            self.__ani.addAni(self.expansion_widget.height(), 0,duration=self.__duration, courseFunc=self.expansion_widget.setFixedHeight)
            self.__flag = False
        self.__ani.start()

    def setButton(self,btn):
        self.btn = btn
        self.btn.setMinimumHeight(self._fh)
        self.btn.clicked.connect(self.stretch_event)

    def setWidget(self,widget:QWidget):
        self.expansion_widget = widget
        self.__vboy.addWidget(self.btn)
        self.__vboy.addWidget(self.expansion_widget)
        self.__vboy.addItem(self._sp)


class Drawer(QScrollArea):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.setWidgetResizable(True)

        self.__core = QWidget()

        self.setWidget(self.__core)

        self._vboy = QVBoxLayout(self.__core)
        self._vboy.setSpacing(0)
        self._vboy.setContentsMargins(0,0,0,0)
        self._sp = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.setHorizontalScrollBarPolicy(qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(qt.ScrollBarAlwaysOff)

    def addItem(self,item:DrawerItem):
        self._vboy.removeItem(self._sp)
        self._vboy.addWidget(item)
        self._vboy.addItem(self._sp)

    def findItem(self,index:int)->DrawerItem:
        return self._vboy.itemAt(index).widget()

    def removeItem(self,item:DrawerItem):
        self._vboy.removeWidget(item)
