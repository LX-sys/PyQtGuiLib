# -*- coding:utf-8 -*-
# @time:2023/3/1817:31
# @author:LX
# @file:superPainter.py
# @software:PyCharm

from PyQtGuiLib.header import (
    QApplication,
    PYQT_VERSIONS,
    sys,
    QPainter
)
from PyQtGuiLib.styles.superPainter.graph import Rect


class SuperPainterABC:
    def __init__(self, parent: QWidget = None):
        self.__parent = None

        self.__painter = QPainter()

    def setParent(self,parent):
        self.__parent = parent

    def parent(self):
        return self.__parent

    def painter(self)->QPainter:
        return self.__painter

    def begin(self,parent=None):
        if parent:
            self.painter().begin(parent)
        else:
            self.painter().begin(self.parent())

    def end(self):
        self.painter().end()


class SuperPainter(SuperPainterABC):
    def __init__(self, parent: QWidget = None):
        super(SuperPainter, self).__init__(parent)


    def drawRect(self,*args,**kwargs):
        obj = Rect(self.painter(),*args,**kwargs)
        obj.draw()
