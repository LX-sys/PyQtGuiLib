# -*- coding:utf-8 -*-
# @time:2023/2/1810:31
# @author:LX
# @file:controlType.py
# @software:PyCharm

from PyQtGuiLib.header import *
from PyQtGuiLib.header.Qt import qtWidgets

app = qtWidgets.QApplication([])
btn = qtWidgets.QPushButton()

class ControlType:
    @staticmethod
    def isWidgetObj(obj)->bool:
        excludes =["PYQT_VERSIONS","QApplication","QWIDGETSIZE_MAX",
                   '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']

        for q in dir(qtWidgets):
            # print(q)
            if q in excludes:
                continue
            if "QAbs" in q:
                continue
            if "__" in q:
                continue
            if "q" in q:
                continue

            if isinstance(obj,eval(q)):
                return True
        return False


# print(dir(qtWidgets))

print(ControlType.isWidgetObj(btn))