# -*- coding:utf-8 -*-
# @time:2023/3/2717:33
# @author:LX
# @file:logBrowser.py
# @software:PyCharm
from PyQtGuiLib.header import (
    QApplication,
    sys,
    PYQT_VERSIONS,
    QWidget,
    QTextBrowser,
    QThread,
    Signal,
    QObject
)
import os
from datetime import datetime as dt


TimeFormat = str



class SendLog(QThread):
    send = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# # 本地日志管理
class LoadLocalLog(QThread):
    loaded = Signal(str)

    def __init__(self, path=".",filename="test.log",encoding="utf8",limit=1000):
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
        path = os.path.join(self.path(),self.fileName())
        with open(path,"r") as f:
            n = 0
            limit = self.limit()
            while n<limit or limit == -1:
                data = f.readline()
                if data:
                    self.loaded.emit(data)
                    self.msleep(1)
                else:
                    break
                n += 1


# 日志控件
class LogBrowser(QTextBrowser):
    Debug = "Debug"
    Info = "Info"
    Warning = "Warning"
    Error = "Error"
    Critical = "Critical"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.__timeFormat = "%Y-%m-%d %H:%M:%S"

        self.ll = LoadLocalLog(limit=-1)
        self.ll.loaded.connect(self.test)
        self.ll.start()

    def test(self,info):
        self.append(info,LogBrowser.Debug)

    def setTimeFormat(self,format:TimeFormat):
        self.__timeFormat = format

    def timeFormat(self) -> TimeFormat:
        return self.__timeFormat

    def append(self, p_str,mode="Info"):
        for_time = dt.strftime(dt.now(),self.timeFormat())
        log = "{mode} [{time}] > {info}".format(mode=mode,
                                            time=for_time,
                                            info=p_str.replace("\n",""))
        super().append(log)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = LogBrowser()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())