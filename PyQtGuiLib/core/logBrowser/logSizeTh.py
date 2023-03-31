# -*- coding:utf-8 -*-
# @time:2023/3/3117:02
# @author:LX
# @file:logSizeTh.py
# @software:PyCharm

'''
    读取日志大小线程
'''

import os
from PyQtGuiLib.header import (
    QThread,
    Signal
)


# 计算日志大小线程
class LogSizeTh(QThread):
    Sizeed = Signal(int)

    def __init__(self, path:str):
        super().__init__()
        self.__path = path

    def setPath(self,path):
        self.__path = path

    def run(self):
        st = os.stat(self.__path)
        self.Sizeed.emit(st.st_size)
