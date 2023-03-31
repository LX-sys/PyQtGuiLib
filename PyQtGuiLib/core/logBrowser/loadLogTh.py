# -*- coding:utf-8 -*-
# @time:2023/3/3117:04
# @author:LX
# @file:loadLogTh.py
# @software:PyCharm
import os
import time
from PyQtGuiLib.header import (
    QThread,
    Signal
)

# 本地日志管理
class LoadLocalLog(QThread):
    loaded = Signal(str)
    finish = Signal()

    def __init__(self, path=".",filename="test.txt",encoding="utf8",limit=1000):
        super().__init__()
        self.__local_log = {
            "path": path,
            "filename": filename
        }
        self.__encoding = encoding
        self.__limit = limit

    def setLimit(self,n:int):
        self.__limit = n

    def limit(self)->int:
        return self.__limit

    def encoding(self) -> str:
        return self.__local_log

    def setLocalFileInfo(self, path, filename):
        self.__local_log["path"] = path
        self.__local_log["filename"] = filename

    def localFileInfo(self) -> dict:
        return self.__local_log

    def path(self) -> str:
        return self.__local_log["path"]

    def fileName(self) -> str:
        return self.__local_log["filename"]

    def run(self):
        old = time.time()
        # print("开始:",old)
        path = os.path.join(self.path(),self.fileName())
        with open(path,"r") as f:
            n = 0
            size = 0
            limit = self.limit()
            while n<limit or limit == -1:
                data = f.readline()
                if data:
                    size += len(data)
                    self.loaded.emit(data)
                    # self.msleep(1)
                else:
                    break
                n += 1
        print("数据量:{} 字节大小:{}".format(n,size))
        new = time.time()
        print("耗时:",new-old)
        self.finish.emit()
